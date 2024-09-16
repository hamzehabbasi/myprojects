from AppBase.usage import usage
from Business.models import BusinessProduct


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
def change_order_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            current_product = BusinessProduct.k(d['product_key'])
            _ = current_product.key
            category_order = int(d['category_order']) if 'category_order' in d.keys() else False
            total_order = int(d['total_order']) if 'total_order' in d.keys() else False

            category = current_product.category
            if not category:
                raise Exception

            if not category_order and not total_order:
                raise KeyError

        except (ValueError, KeyError, AttributeError):
            return 400

    if "Check For Category Order" and category_order:
        if 'Rearrange  Products Order':
            category_products = category.category_products.A()
            changed_products = [current_product]

        if current_product.category_order == category_order:
            return 200, category.api()

        if current_product.category_order > category_order:
            for product in category_products:
                if category_order <= product.category_order < current_product.category_order:
                    product.category_order += 1
                    changed_products.append(product)

        else:
            for product in category_products:
                if category_order >= product.category_order > current_product.category_order:
                    product.category_order -= 1
                    changed_products.append(product)

        current_product.category_order = category_order

        BusinessProduct.objects.bulk_update(changed_products, ['category_order'])
        customer.save_synchronize_flag("categories", customer.pk)

        if "Done":
            return 200, category.api()

    if "Check For Total Order" and total_order:
        if 'Rearrange  Products Order':
            business_products = BusinessProduct.A()
            changed_products = [current_product]

        if current_product.total_order == total_order:
            return 200, [x.key for x in category.business.products.A().order_by('total_order')]

        if current_product.total_order > total_order:
            for product in business_products:
                if total_order <= product.total_order < current_product.total_order:
                    product.total_order += 1
                    changed_products.append(product)

        else:
            for product in business_products:
                if total_order >= product.total_order > current_product.total_order:
                    product.total_order -= 1
                    changed_products.append(product)

        current_product.total_order = total_order
        BusinessProduct.objects.bulk_update(changed_products, ['total_order'])
        customer.save_synchronize_flag("categories", customer.pk)

        if "Done":
            return 200, [x.key for x in category.business.products.A().order_by('total_order')]
