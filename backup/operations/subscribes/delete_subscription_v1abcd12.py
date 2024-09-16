from AppBase.usage import usage
from Business.models import Subscription


@usage
def delete_subscription_v1abcd12(request, d, device):
    try:
        subscription = Subscription.k(d["subscription_key"])

        if subscription.service.provider.id == device.user.id or subscription.customer.id == device.user.id:

            subscription.trashed = True
            subscription.save()

            return [200, {"message": "successfully_deleted"}]
        else:
            return 401
    except:
        return 404, {"msg": "Not Found"}
