from AppBase.usage import usage
from Business.models import VitrineCategory, BusinessProduct, SubscriptionService


@usage
def delete_category_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            category = VitrineCategory.k(d['key'])

            if not category:
                return 200

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Delete':
        if "Have Products":
            products = BusinessProduct.f(category__exact=category)
            if products:
                for product in products:
                    product.category = None

                BusinessProduct.objects.bulk_update(products, ['category'])

        if "Have Services":
            services = SubscriptionService.f(category__exact=category)
            if services:
                for service in services:
                    service.category = None

                SubscriptionService.objects.bulk_update(services, ['category'])

        category.trashed = True
        category.save()

    return 200
