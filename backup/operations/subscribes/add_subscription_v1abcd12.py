from datetime import datetime, timedelta

from django.db.models import Sum

from AppBase.usage import usage
from Business.models import Subscription, SubscriptionServiceCostModel, \
    iTSubscription, SubscriptionService
from Business.text import CHECKOUT_SUBSCRIPTION_WELCOME_LEAD, subscription_title_generator
from Platform.models import iTransaction, User
from toolkit import load_request_payment_flags


@usage
def add_subscription_v1abcd12(request, d, device):
    try:
        mobile = d["mobile"] if 'mobile' in d.keys() else False
        customer_name = d["customer_name"] if 'customer_name' in d.keys() else False
        cost_model = SubscriptionServiceCostModel.g(key__exact=d['cost_model'])
        service = cost_model.service
        token = d['token'] if 'token' in d.keys() else ""
        by_virdaar, by_card = load_request_payment_flags(d)
    except:
        return 400

    if 'Verify Customer Account or Make an account for him/her':
        try:
            customer = device.user
            mobile = customer.mobile
        except AttributeError:
            customer = User.find_user(mobile)
            if customer:
                return 405

            if not customer_name or not mobile:
                return 400
            parameters, template_id = CHECKOUT_SUBSCRIPTION_WELCOME_LEAD(customer_name)
            customer, device = User.lead(
                mobile,
                customer_name,
                request,
                parameters,
                template_id
            )

    transaction_amount = cost_model.cost

    subscription = Subscription.g(service__exact=service, customer__exact=customer)

    if 'Direct Buy By VIRDAR Units':
        virdaar_amount = 0
        if by_virdaar == 1:
            virdaar_amount = transaction_amount
            transaction_amount = 0

    if "Calculate Amount Add Amount To Reqeust":
        transaction_amount = transaction_amount + virdaar_amount
        d['amount'] = transaction_amount

    if "Check Balance":
        balance_status, balance_response, virdaar_checkout, off_data = customer.check_balance(
            virdaar=virdaar_amount,
            cash=transaction_amount,
            service_id=service.key,
            by_card={"request": d, "state": by_card, "device": device},
            tax=True if service.key != 'cr' else False
        )

        if balance_status != 200:
            return balance_status, balance_response

    tax = 0
    if "Calculate Tax" and service.key != 'cr':
        it_gifts = balance_response
        gift_amount = it_gifts.aggregate(Sum('amount'))['amount__sum'] if it_gifts else 0
        off_amount = off_data['off'] if off_data else 0

        tax = round(((transaction_amount - gift_amount - off_amount) * 9) / 100, 4)

    if "Create iTransaction":
        transaction = iTransaction(
            amount=transaction_amount,
            tax=tax,
            src=customer,
            dst_id=1,
            trans_type="subscription",
            trashed=True
        )
        transaction.save()

    if "Calculate Expire":
        expire = datetime.now() + timedelta(days=cost_model.interval)
        if not subscription:
            subscription = Subscription(
                service=service,
                expire=expire,
                customer=customer,
                cost_model=cost_model,
            )

            subscription_title = subscription_title_generator(subscription)
            subscription.title = subscription_title
            subscription.save()

        else:
            if not subscription.available:
                return 406

            if subscription.expire <= datetime.now():
                subscription.expire = expire

            else:
                subscription.expire += timedelta(days=cost_model.interval)

    if "Create iTSubscription":
        subscription_transaction = iTSubscription(
            transaction=transaction,
            subscription=subscription,
            expire=subscription.expire,
            base_price=cost_model.cost,
            cost_model_ilink=cost_model.key
        )
        subscription_transaction.save()

    if "Calculate and Update Subscription's Config":
        subscription.cost_model = cost_model
        if service.key == 'cj':
            subscription.config['title'] = cost_model.config['title']
            subscription.update_config()

        elif service.key == 'cr':
            subscription.config['total_days'] += cost_model.interval
            subscription.config['total_credit'] += cost_model.cost
            subscription.config['remained_credit'] += cost_model.cost

        subscription.save()

    if "Update Flags":
        SubscriptionService.update_flag(customer)
        service.update = datetime.now()
        service.save()

    if "Done":
        transaction.trashed = False
        transaction.affect_off(off_data)
        transaction.save()
        customer.update_balance()

    return 200, {"link": service.callback + "?token=" + token}
