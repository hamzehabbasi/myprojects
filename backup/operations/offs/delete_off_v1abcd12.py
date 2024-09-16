from AppBase.usage import usage
from Business.models import Off


@usage
def delete_off_v1abcd12(req, d, device):
    try:
        customer = device.user
    except AttributeError:
        return 401

    try:
        discount = Off.ag(key__exact=d['key'], business__customer__exact=customer)
        _ = discount.business
    except (AttributeError, KeyError):
        return

    if discount.trashed:
        return 200

    discount.trashed = True
    discount.save()

    return 200
