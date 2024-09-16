from AppBase.usage import usage
from Business.models import BusinessProductLabel


@usage
def delete_label_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            label = BusinessProductLabel.g(key__exact=d['label_key'], business__customer__exact=customer)
            _ = label.business
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Delete':
        label.trashed = True
        label.save()

    return 200
