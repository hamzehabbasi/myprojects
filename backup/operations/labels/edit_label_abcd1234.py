from AppBase.usage import usage
from Business.models import BusinessProductLabel


def api(self):
    return {
        "key": self.key,
        "name": self.name,
        "color": self.color,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed,
        "business": self.business.key
    }


@usage
def edit_label_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            label = BusinessProductLabel.g(key__exact=d['label_key'], business__customer__exact=customer)
            _ = label.business

            name = d['name']
            color = d['color']
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Save':
        label.name = name
        label.color = color if color else label.color
        label.save()

        return label.api()
