from datetime import datetime

from django.utils import timezone

from Business.models import Business, BusinessProduct, iTProduct, SubscriptionService, Off, iTOff
from Business.models import SubscriptionServiceCostModel, iTSubscription, Subscription, Order, iTManual
from Business.operations.offs.buy_affect_offs_abcd1234 import buy_affect_offs_abcd1234
from Business.text import subscription_title_generator, successful_buy_notification
from Payment.models import iTTransfer
from Platform.models import Cache, iTransaction, iTGift
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


def buy_virdar_customer_v1abcd12(_, d, device):
    if "Validate Request and Initialize":
        # try:
        cache = Cache.g(token__exact=d['key'], device__exact=device)

        business = Business.k(cache.business_ilink)
        config = business.subscription.config['features']
        customer = device.user

        validate = cache and business and customer
        if not validate:
            raise ValueError

        if 'amount' in d.keys() and d['amount'] == 0 or cache.data["order"]["amount"] <= 0:
            return 405

        by_virdaar, by_card = load_request_payment_flags(d)
        # except (AttributeError, ValueError, KeyError):
        #     return 400

    if "Verification of Request":
        if cache.expire_time < datetime.now():
            return 401

        if 'state' in cache.data.keys() and cache.data['state'] == 'paid':
            return 401

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
        if "Update off Data":
            Off.off_updater(cache.data['order'], business)

        cache = buy_affect_offs_abcd1234(
            cache=cache,
            business=business,
            customer=None,
            off_code=cache.data["code"] if 'code' in d.keys() else None
        )
        cache.calculate_total_amount(business.subscription.config)

    if "Check for Balance":
        cash_amount = cache.data["order"]["amount"] - cache.data["order"]["off"] + cache.data['order']["cashback"]
        cash_amount = round(cash_amount, 4)

    if "validate amount cache":
        if "Check For 100% Off" and cash_amount == 0 and cache.data["order"]["amount"] > 0:
            by_virdaar = by_card = 0
            transaction = iTransaction(
                amount=round(cache.data["order"]["commission"], 4),
                trans_type="transfer",
                src=business.customer,
                dst=customer,
                trashed=True
            )
            transaction.save()

            transfer = iTTransfer(
                transaction=transaction,
                asset="money",
                description=f"{'بابت کمیسیون سفارش'} {cache.data['token']}",
                state="accepted"
            )
            transfer.save()

            transaction.trashed = False
            transaction.save()

            customer.update_balance()

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
        if "Search For Order By Key":
            order = Order.ki(cache.data['token'])
            if "Exist Order" and order:
                order.customer = customer
                order.business = business
                order.amount = cache.data["order"]["amount"]
                order.trashed = True
                order.save()

            else:
                order = Order(
                    customer=customer,
                    business=business,
                    amount=cache.data["order"]["amount"],
                    key=cache.data['token'],
                    trashed=True
                )
                order.save(not_generate_key=True)

        transactions = []
        cashback_data = []

    if "Has Additional Amount" and config['additionalAmount']:
        if cache.data['order']['manual']['amount'] > 0:
            it_manual_transaction = iTransaction(
                amount=round(cache.data['order']['manual']['amount'], 4),
                commission=round(cache.data['order']['additional_amount_commission'], 4),
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
                    it_off = iTOff(
                        off_amount=cache.data['order']['manual']['off'],
                        transaction=it_manual_transaction,
                        is_additional=True
                    )

                    it_off.save()

            transactions.append(it_manual_transaction)

    if "Has Product in Order" and config['products']:
        for each in cache.data['order']['products']:
            if "Create iTransaction":
                itransaction = iTransaction(
                    amount=round(each['amount'] - each['commission'], 4),
                    commission=round(each['commission'], 4),
                    tax=0,
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
                            "amount": each['off']
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

                SubscriptionService.update_flag(customer)
                service.update = datetime.now()
                service.save()

                service.provider.customer.save_synchronize_flag("subscriptions", service.key)

            if 'Create iTransaction':
                itransaction = iTransaction(
                    amount=round(each['amount'] - each['commission'], 4),
                    commission=round(each['commission'], 4),
                    tax=0,
                    src=customer,
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
            amount=round(amount, 4),
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

    if "Check Loyal Customers":
        order.purchase_number = Order.f(business__exact=business, customer__exact=device.user).count() + 1

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

    if "Done":
        if config['waitingAfterPayment']:
            cache.data['state'] = 'waiting'
        else:
            cache.data['state'] = 'paid'
            cache.expire_time = datetime.now()

        cache.data['paid'] = paid_amount
        cache.save()

        if "Send Message For Business Owner":
            parameters, template_id = successful_buy_notification(customer, order.token, cache.data['order'])
            # send_message(business.customer.mobile, parameters, template_id)

        return order.buyer_api_v2()  # @todo
