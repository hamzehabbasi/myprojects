from AppBase.usage import usage
from Business.models import Subscription, iTSubscription, iTSubscriptionCancel
from Platform.models import iTransaction, User


@usage
def cancel_subscription_v1abcd12(request, d, device):
    try:
        customer = device.user
    except:
        return 401

    try:
        subscription = Subscription.k(d['subscription_key'])
        order = d['order']
    except:
        return 400

    if not subscription:
        return 401

    if not subscription or \
            (subscription.customer != customer and
             subscription.service.provider.customer != customer):
        return 401

    cost_model = subscription.cost_model
    if order == 0:
        remaining_duration = (subscription.expire - subscription.create).days
        total_duration = cost_model.interval
        amount = (remaining_duration * cost_model.cost) / total_duration
    else:
        amount = cost_model.cost

    virdaar = User.i(1)
    cancel_itransaction = iTransaction(
        amount=amount,
        src=virdaar,
        dst_id=customer.id,
        trans_type="cancel_subscription"
    )
    cancel_itransaction.save()
    customer.update_balance()

    canceled_itsubscription = iTSubscription.g(subscription__exact=subscription)

    it_subscription_cancel = iTSubscriptionCancel(
        canceled_itsubscription=canceled_itsubscription,
        transaction=cancel_itransaction
    )
    it_subscription_cancel.save()

    subscription.trashed = True
    subscription.save()

    return 200
