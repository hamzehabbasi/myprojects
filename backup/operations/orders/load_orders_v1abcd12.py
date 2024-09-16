from AppBase.usage import usage

from Business.models import Order


def seller_api(self):
    products = [product.order_seller_api() for product in self.product_orders.A()]

    subscriptions = self.subscription_orders.A().select_related('subscription')
    subscriptions = [subscription.order_seller_api() for subscription in subscriptions]
    manual = self.manual_orders.g()
    order_data = self.order_cache.data['order'] if self.order_cache else {}
    return {
        "key": self.key,
        "customer": self.customer.api(),
        "business_key": self.business.key if self.business else False,
        "amount": self.amount,
        "products": products,
        'manual': manual.order_seller_api() if manual else None,
        'total_off': order_data['off'] if self.order_cache else 0,
        'additional_discount': order_data['additional_discount']['amount'] if self.order_cache else 0,
        "subscriptions": subscriptions,
        "turn_number": self.turn_number,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "purchase_number": self.purchase_number
    }


@usage
def load_orders_v1abcd12(_, d, device):
    if 'Partial Fetch':
        try:
            keys = d['keys']
        except KeyError:
            keys = None

    orders = Order.objects.none()

    if 'Partial Fetch' and keys:
        orders = Order.af(business__customer__exact=device.user).af(key__in=d['keys'])

    if 'Full Fetch' and not keys:
        orders = Order.f(business__customer__exact=device.user)

    return [x.seller_api() for x in orders.order_by('update')]
