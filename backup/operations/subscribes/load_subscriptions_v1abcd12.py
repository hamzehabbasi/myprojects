from datetime import datetime
from itertools import chain

from AppBase.usage import usage
from Business.models import Subscription, Business
from Business.text import *


def api(self, customer):
    try:
        last_paid = self.subscription_transactions.order_by('-create')[0].create.timestamp()
    except:
        if self.service.key == 'cj':
            last_paid = self.create.timestamp()
        else:
            last_paid = None

    business = self.service.provider
    self.config['remained_days'] = max(0, (self.expire - datetime.now()).days)
    response = {
        "key": self.key,
        "title": self.title,
        "service": self.service.key,
        "expire": self.expire.timestamp(),
        "last_paid": last_paid,
        "cost_model": self.cost_model.key,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "config": self.config,  # @todo
        "available": self.available,
        "active": not self.trashed,
        "business": {
            "key": business.key,
            "role": "buyer",
            "cover": (settings.VIRDAAR_ENDPOINT_URL + business.cover.name) if business.cover else False,
            "title": business.title
        },
        "consumed_limitation": None
    }

    if "As Business Manager" and customer != self.customer:
        response["business"] = {
            "key": business.key,
            "role": "seller"
        }

        if "Calculate Limitation":
            business_as_customer = Business.g(subscription_ilink__exact=self.key)
            if business_as_customer:
                consumed = business_as_customer.business_orders.A().count()
                if consumed:
                    response["consumed_limitation"] = consumed

        response["customer"] = self.customer.api(more_fields=[
            'address',
            'mobile',
            'fathername',
            'birthday',
            'national_id'
        ])

    return response


@usage
def load_subscriptions_v1abcd12(_, d, device):
    customer = device.user

    if 'Partial Fetch':
        try:
            keys = d['keys']
        except KeyError:
            keys = None

    if 'Customer Subscribes':
        subscriptions = customer.customer_subscriptions.all().exclude(id=64)

        if keys:
            subscriptions = subscriptions.af(key__in=keys)

        subscriptions = subscriptions.select_related(
            'service',
            'cost_model',
            'customer'
        )

    if 'Business Customer Subscribes':
        business_keys = [x.key for x in customer.businesses.all()]
        business_subscriptions = Subscription.f(service__provider__key__in=business_keys)
        if keys:
            business_subscriptions = business_subscriptions.af(key__in=keys)

        business_subscriptions = business_subscriptions.select_related(
            'service',
            'cost_model',
            'customer'
        )

    if 'Make API and Sort':
        items = list(chain(subscriptions, business_subscriptions))
        items = [x.api(customer) for x in items]

        return sorted(items, key=lambda x: x["create"])
