from AppBase.usage import usage
from Business.models import VitrineCategory, Business


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
def add_category_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
            name = d['name']
            business_key = d['business_key']
            business = Business.k(business_key)
            if not business:
                raise KeyError

            if business.customer != customer:
                raise AttributeError

            if not name:
                raise ValueError

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Save':
        category = VitrineCategory(
            name=name,
            business=business
        )
        category.save()

    return 200, category.api()
