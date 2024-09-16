from datetime import datetime, timedelta

from AppBase.usage import usage
from Business.operations.subscribes.add_subscription_v1abcd12 import add_subscription_v1abcd12
from Platform.models import Cache, User, Prompt, Device


@usage
def checkout_subscription_form_v1abcd12(request, d, device):
    try:
        mobile = d["mobile"]
        fullname = d["fullname"]
        username = d["username"] if 'username' in d.keys() else mobile
        prompt = Prompt.k(d['prompt_key'])
        token = d['token']
    except:
        return 400

    cache = Cache.g(token__exact=token)

    if prompt.cache.token != token:
        return 401

    d = {
        "cost_model": cache.data["cost_model"]["key"],
        "service_key": cache.data["subscription_service"]["key"],
        "token": cache.token
    }

    user = User(
        username=username
    )
    user.save()
    user.meta_update("fullname", fullname)
    user.meta_update("mobile", mobile)

    device = Device(
        user=user,
        agent="checkout_subscription_form" + token,
    )
    device.save()

    d["by_card"] = 1

    device.expire = datetime.now() + timedelta(seconds=30)
    device.save()

    return add_subscription_v1abcd12(request, d, device)
