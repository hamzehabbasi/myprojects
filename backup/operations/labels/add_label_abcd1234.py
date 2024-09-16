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
def add_label_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            business = customer.businesses.k(d['key'])
            _ = business.key

            name = d['name']
            color = d['color']

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Save':
        label = BusinessProductLabel(
            name=name,
            business=business,
            color=color,
        )
        label.save()

        return label.api()
