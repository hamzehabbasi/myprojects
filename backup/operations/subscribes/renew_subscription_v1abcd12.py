from datetime import datetime, timedelta

from django.db.models import Sum

from AppBase.usage import usage
from Business.models import Subscription, SubscriptionServiceCostModel, \
    iTSubscription, SubscriptionService
from Platform.models import iTransaction
from toolkit import load_request_payment_flags


@usage
def renew_subscription_v1abcd12(request, d, device):
    try:
        customer = device.user
        cost_model = SubscriptionServiceCostModel.k(d['cost_model'])
        service = cost_model.service
        subscription = d["subscription_key"]
        d['amount'] = cost_model.cost
        d['service_key'] = service.key
        subscription = Subscription.k(subscription)

    except (KeyError, AttributeError, ValueError):
        return 400

    if "Check For Subscription Availability":
        try:
            if not subscription.available:
                return 406
        except AttributeError:
            return 400

    transaction_amount = cost_model.cost
    by_virdaar, by_card = load_request_payment_flags(d)

    if 'Direct Buy by VIRDAR units':
        virdaar_amount = 0
        if by_virdaar == 1:
            virdaar_amount = transaction_amount
            transaction_amount = 0

    if "Calculate Tax And Add Amount To Reqeust" and service.key != 'cr':
        tax = ((transaction_amount + virdaar_amount) * 9) / 100
        d['amount'] = transaction_amount + virdaar_amount + tax

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

    if "Set New Config For Subscription":
        subscription.cost_model = cost_model
        if service.key == 'cj':
            subscription.config['title'] = cost_model.config['title']
            subscription.update_config()

        elif service.key == 'cr':
            subscription.config['total_days'] += cost_model.interval
            subscription.config['total_credit'] += cost_model.cost
            subscription.config['remained_credit'] += cost_model.cost

        else:
            subscription.config = subscription.cost_model.config

        subscription.save()

    if "Done":
        transaction.trashed = False
        transaction.affect_off(off_data)
        transaction.save()

    if "Update Flags":
        SubscriptionService.update_flag(customer)
        service.update = datetime.now()
        service.save()

    customer.update_balance()
    print(customer.cash)
    return 200, {}
