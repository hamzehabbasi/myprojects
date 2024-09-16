from AppBase.usage import usage
from Business.models import VitrineCategory


def api(self):
    return {
        "key": self.key,
        "name": self.name,
        "business_key": self.business.key,
        "products": [x.key for x in self.category_products.A().order_by("order")],
        "create": self.create.timestamp(),
        "update": self.update.timestamp()
    }


@usage
def load_categories_v1abcd12(_, d, device):
    if 'Partial Fetch':
        try:
            keys = d['keys']
        except KeyError:
            keys = None

    categories = VitrineCategory.objects.none()

    if 'Partial Fetch' and keys:
        categories = VitrineCategory.af(business__customer__exact=device.user).af(key__in=d['keys'])

    if 'Full Fetch' and not keys:
        categories = VitrineCategory.f(business__customer__exact=device.user)

    return [x.api() for x in categories.order_by('update')]
