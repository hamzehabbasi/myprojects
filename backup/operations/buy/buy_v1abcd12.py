from datetime import datetime

from django.utils import timezone

from AppBase.usage import usage
from Business.models import Business, BusinessProduct, iTProduct, SubscriptionService, Off, iTOff
from Business.models import SubscriptionServiceCostModel, iTSubscription, Subscription, Order, iTManual
from Business.operations.offs.buy_affect_offs_abcd1234 import buy_affect_offs_abcd1234
# from Business.operations.offs import buy_affect_offs
from Business.text import subscription_title_generator
from Payment.models import Sim
from Platform.models import Cache, iTransaction, User, iTGift
from toolkit import load_request_payment_flags


def buyer_api_v2(self):
    products = [each.buyer_api_v2(self.customer) for each in self.product_orders.A()]

    it_subscriptions = self.subscription_orders.A().select_related('subscription')
    subscriptions = [each.buyer_api_v2(self.customer) for each in it_subscriptions]

    return {
        "key": self.key,
        "customer": self.customer.api(),
        "business_key": self.business.key if self.business else False,
        "amount": self.amount,
        "products": products,
        "subscriptions": subscriptions,
        "turn_number": self.turn_number,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "purchase_number": self.purchase_number
    }


@usage
def buy_v1abcd12(_, d, device):
    if "Validate Request and Initialize":
        try:
            cache = Cache.g(token__exact=d['key'], device__exact=device)

            business = Business.k(cache.business_ilink)
            config = business.subscription.config['features']

            mobile = d["mobile"] if 'mobile' in d.keys() else None
            fullname = d["fullname"] if 'fullname' in d.keys() else None
            validate_mobile = mobile is None or (type(mobile) is str and len(mobile) == 11)

            validate = cache and business and validate_mobile
            if not validate:
                raise ValueError

            if 'amount' in d.keys() and d['amount'] == 0:
                return 405

            by_virdaar, by_card = load_request_payment_flags(d)
        except (AttributeError, ValueError, KeyError):
            return 400

    if "Verification of Request":
        if cache.expire_time < datetime.now():
            return 401

        if 'state' in cache.data.keys() and cache.data['state'] == 'paid':
            return 401

    if "Verify Customer Account":
        try:
            if not device and mobile:
                sim = Sim.g(mobile__exact=mobile)
                if sim:
                    customer = sim.customer
                else:
                    customer = User(username=mobile)
                    customer.save()
                    if fullname:
                        customer.meta_update('fullname', fullname)
            else:
                customer = device.user
        except AttributeError:
            return 406

    if "Prepare for Payment":
        cache.data['state'] = 'on_payment'
        cache.calculate_total_amount(business.subscription.config)
        cache.save()

    if "Verify Order Items Availability":
        if "Check Products" and config['products']:
            for each in cache.data['order']['products']:
                product = BusinessProduct.k(each['key'])
                product_stock = product.stock if product.stock else 0
                if product_stock <= 0:
                    for item in cache.data['order']['products']:
                        if product.key in item.keys():
                            cache.data['order']['products'].remove(item)

                    continue

                if product.stock is not None and product.stock < each["count"]:
                    return 406

                if product.business_ilink != business.key:
                    return 401

        if "Check Services" and config['subscriptions']:
            for each in cache.data['order']['services']:
                cost_model = SubscriptionServiceCostModel.k(each['cost_model_key'])
                service = SubscriptionService.k(each['key'])

                if cost_model.service.key != service.key:
                    return 401

                if service.provider.key != business.key:
                    return 401

    if "Verify Offs Availability" and config['offs']:
        cache = buy_affect_offs_abcd1234(
            cache=cache,
            business=business,
            customer=None,
            off_code=cache.data["code"] if 'code' in d.keys() else None
        )
        cache.calculate_total_amount(business.subscription.config)

    if "Check for Balance":
        total_commission = cache.data["order"]["commission"] + cache.data["order"]["additional_amount_commission"]
        cash_amount = cache.data["order"]["amount"] - cache.data["order"]["off"] + total_commission

    if "validate amount cache":
        if cash_amount == 0:
            return 405

        if 'Direct Buy by VIRDAR units':
            virdaar_amount = 0
            if by_virdaar == 1:
                virdaar_amount = cash_amount
                cash_amount = 0

        balance_status, balance_response, virdaar_checkout, _ = customer.check_balance(
            virdaar=virdaar_amount,
            cash=cash_amount,
            by_card={"request": d, "state": by_card, "device": device},
            business=business
        )

        if balance_status != 200:
            return balance_status, balance_response

    if "Create Order":
        if 'renew_order' in cache.data.keys():
            order = Order.k(cache.data['token'])
            if "Check For Previous Order And Transactions":
                if order:
                    it_products = order.product_orders.A()
                    it_subscriptions = order.subscription_orders.A()
                    it_manual = iTManual.g(order__exact=order)

                    if it_products:
                        for it in it_products:
                            it.trashed = True
                        iTProduct.objects.bulk_update(it_products, ['trashed'])

                    if it_subscriptions:
                        for it in it_subscriptions:
                            it.trashed = True
                        iTSubscription.objects.bulk_update(it_subscriptions, ['trashed'])

                    if it_manual:
                        it_manual.trashed = True
                        it_manual.save()

        else:
            order = Order(
                customer=customer,
                business=business,
                amount=cache.data["order"]["amount"],
                key=cache.data['token'],
                purchase_number=cache.data["purchase_number"],
                trashed=True
            )
            order.save(not_generate_key=True)

            cache.data['order']['order_key'] = order.key
        transactions = []
        cashback_data = []

    if "Has Additional Amount" and config['additionalAmount']:
        if cache.data['order']['manual']['amount'] > 0:
            amount = cache.data['order']['manual']['amount'] * (1 - cache.data['order']['additional_amount_commission'])
            it_manual_transaction = iTransaction(
                amount=amount,
                commission=cache.data['order']['additional_amount_commission'],
                src=customer,
                dst=business.customer,
                trans_type="manual",
                trashed=True
            )
            it_manual_transaction.save()

            it_manual = iTManual(
                order=order,
                transaction=it_manual_transaction,
                amount=cache.data['order']['manual']['amount']
            )
            it_manual.save()

            if "Has Off" and cache.data['order']['manual']['off'] > 0:
                if "Add Off to Transaction":
                    it_manual_transaction.off_ilink = cache.data['order']['manual']['key']
                    it_manual_transaction.off_amount = cache.data['order']['manual']['off']
                    it_manual_transaction.off_type = "direct"

                if "Affect Off":
                    Off.off_updater(cache.data['order']['manual'], business)

            transactions.append(it_manual_transaction)

    if "Has Product in Order" and config['products']:
        for each in cache.data['order']['products']:
            if "Create iTransaction":
                itransaction = iTransaction(
                    amount=each['amount'] - each['commission'],
                    commission=each['commission'],
                    src=customer,
                    dst=business.customer,
                    trans_type="product",
                    trashed=True,
                )
                itransaction.save()

            if "Create iTProduct":
                product = BusinessProduct.k(each['key'])
                it_product = iTProduct(
                    transaction=itransaction,
                    product=product,
                    count=each["count"],
                    order=order,
                    base_price=each["base_price"]
                )
                it_product.cost = product.cost if product.cost else 0

                it_product.save()

                if product.stock:
                    product.stock -= each["count"]

                product.save()

            if "Has Off" and each['off'] > 0:
                if "Add Off to Transaction":
                    off = Off.k(each['off_data']['key']) if 'key' in each['off_data'].keys() else None
                    if off and off.affect_type == 'direct':
                        it_off = iTOff(
                            off_amount=each['off'],
                            off=off,
                            transaction=itransaction,
                            is_additional=False if off else True
                        )
                        it_off.save()

                    if off and off.affect_type == 'cashback':
                        cashback_data.append({
                            "off_key": off.key,
                            "amount": each['off'],
                            "order_amount": cache.data["order"]["amount"]
                        })

                    elif off and off.affect_type == 'virdarback':
                        pass

            transactions.append(itransaction)

    if "Has Service in Order" and config['subscriptions']:
        for each in cache.data['order']['services']:
            cost_model_key = each['cost_model_key']

            cost_model = SubscriptionServiceCostModel.k(cost_model_key)
            service = cost_model.service
            expire = timezone.now() + timezone.timedelta(days=cost_model.interval)

            if "Check for Subscription":
                subscription = Subscription.g(cost_model__exact=cost_model, service__exact=service)
                if not subscription:
                    subscription = Subscription(
                        service=service,
                        expire=expire,
                        customer=customer,
                        cost_model=cost_model,
                    )
                    is_new = True
                else:
                    if subscription.expire <= datetime.now():
                        subscription.expire = expire
                    else:
                        subscription.expire += timezone.timedelta(days=cost_model.interval)

                    is_new = False

                subscription_title = subscription_title_generator(subscription)
                subscription.title = subscription_title
                subscription.save()

            if 'Create iTransaction':
                itransaction = iTransaction(
                    amount=each['amount'] - each['commission'],
                    src=customer,
                    commission=each['commission'],
                    dst=business.customer,
                    trans_type="subscription",
                    trashed=True
                )
                itransaction.save()

            if "Create iTSubscription":
                it_subscription = iTSubscription(
                    subscription=subscription,
                    transaction=itransaction,
                    order=order,
                    base_price=cost_model.cost
                )

                it_subscription.save()

            if "Add Off to Subscription" and each['off'] > 0:
                off = Off.k(each['off_data']['key']) if 'key' in each['off_data'].keys() else None
                if off and off.affect_type == 'direct':
                    it_off = iTOff(
                        off_amount=each['off'],
                        off=off,
                        transaction=itransaction,
                        is_additional=False if off else True
                    )
                    it_off.save()

                if off and off.affect_type == 'cashback':
                    cashback_data.append({
                        "off_key": off.key,
                        "amount": each['off']
                    })

                elif off and off.affect_type == 'virdarback':
                    pass

            transactions.append(itransaction)

    if "Has CashBack Off" and cashback_data:
        amount = sum([x['amount'] for x in cashback_data])

        off_data = []
        for item in cashback_data:
            key = item['off_key']
            try:
                gift = next(item for item in off_data if item['off_key'] == key)
            except StopIteration:
                gift = False

            if not gift:
                off_data.append({
                    'off_key': key,
                    'amount': item['amount']
                })
            else:
                gift['amount'] += item['amount']

        it_cashback = iTransaction(
            amount=amount,
            src=business.customer,
            dst=customer,
            trans_type='gift'
        )
        it_cashback.save()

        it_gift = iTGift(
            transaction=it_cashback,
            amount=amount,
            expire=business.subscription.expire,
            description='cashback_gift',
            config={
                'for_business': business.key,
                'off_data': off_data
            }
        )
        it_gift.save()

    if "Business Supports Turn" and config["turn"]:
        order.turn_number = cache.data["turn_number"]

    if "Save":
        order.token = cache.data['token']
        order.trashed = False
        order.save()

        paid_amount = 0
        for transaction in transactions:
            paid_amount += float(transaction.amount + transaction.commission)
            transaction.trashed = False

        iTransaction.objects.bulk_update(transactions, ['trashed'])

    if "Update Balance of Customer and Business":
        customer.update_balance()
        business.customer.update_balance()

    # # check for prompt
    # recent_transactions = iTransaction.f(
    #     src=customer,
    #     dst=business.customer,
    #     trans_type="business"
    # )
    #
    # # suggest offer for loyal customers "restaurants"
    # if business.subscription.service.key in ['Rs', 'rs']:
    #     recent_itbusiness_products = iTBusiness.f(
    #         transaction__in=recent_transactions,
    #         product_has__exact=True
    #     )
    #
    #     if len(recent_itbusiness_products) == 2:
    #         prompt = Prompt.g(
    #             customer__exact=business.customer,
    #             type__exact='suggest_off_for_loyal_customers'
    #         )
    #
    #         if not prompt:
    #             data = {
    #                 'message': 'شما میتونین به مشتری های وفادار خودتون تخفیف های خاص بدین !'
    #             }
    #
    #             prompt = Prompt.generate(
    #                 user=business.customer,
    #                 prompt_type='suggest_off_for_loyal_customers',
    #                 data=data
    #             )
    #
    # # suggest offer for loyal customers "academies and clubs"
    # if business.subscription.service.key in ['Ai', 'Bb']:
    #     recent_itbusiness_subscriptions = iTBusiness.f(
    #         transaction__in=recent_transactions,
    #         has_subscription__exact=True
    #     )
    #
    #     if len(recent_itbusiness_subscriptions) == 2:
    #         prompt = Prompt.g(
    #             customer__exact=business.customer,
    #             type__exact='suggest_off_for_loyal_customers'
    #         )
    #
    #         if not prompt:
    #             data = {
    #                 'message': 'شما میتونین به منظور تشویق مشتری های وفادار خودتون از  تخفیف تدریجی استفاده کنین !'
    #             }
    #
    #             prompt = Prompt.generate(
    #                 user=business.customer,
    #                 prompt_type='suggest_gradual_off_for_loyal_customers',
    #                 data=data
    #             )
    #
    # if fullname and mobile:
    #     header = 'عزیز {}'.format(fullname)
    #     body = 'رسید خرید شما از {1} از طریق اپلیکیشن ویردار در دسترس شماست:\n{0}'.format('https://virdaar.ir',
    #                                                                                       business.title)
    #     footer = 'ویردار، فناوری برای زندگی'
    #     send_sms(mobile, header + body + footer)

    if "Done":
        if config['waitingAfterPayment']:
            cache.data['state'] = 'waiting'
        else:
            cache.data['state'] = 'paid'
            cache.expire_time = datetime.now()

        cache.data['paid'] = paid_amount
        cache.save()
        return order.buyer_api_v1()  # @todo
