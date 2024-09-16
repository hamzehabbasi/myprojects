from AppBase.usage import usage
from Business.models import BusinessProductLabel


def order_by(self, *field_names):
    """Return a new QuerySet instance with the ordering changed."""
    if self.query.is_sliced:
        raise TypeError("Cannot reorder a query once a slice has been taken.")
    obj = self._chain()
    obj.query.clear_ordering(force=True, clear_default=False)
    obj.query.add_ordering(*field_names)
    return obj


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
def load_labels_abcd1234(_, __, device):
    labels = BusinessProductLabel.af(business__customer__exact=device.user)
    return [x.api() for x in labels.order_by('update')]
