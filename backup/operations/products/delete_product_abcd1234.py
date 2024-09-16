from AppBase.usage import usage
from Business.models import BusinessProduct


@usage
def delete_product_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            product = BusinessProduct.ag(key__exact=d['product_key'], business__customer__exact=customer)
            if product.trashed:
                return 200

            _ = product.key
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Clean Uploaded Image':
        if product.image and product.image.url.startswith("https"):
            product.image.delete(save=True)

    if 'Clean Product Labels':
        product.labels.clear()

    if 'Delete':
        product.trashed = True
        product.save()

    return 200
