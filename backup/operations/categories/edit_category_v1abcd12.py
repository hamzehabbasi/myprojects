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
def edit_category_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            category = VitrineCategory.k(d['category_key'])
            _ = category.key

            name = d['name']
            if not name:
                raise ValueError

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Save':
        category.name = name
        category.save()

        return 200, category.api()
