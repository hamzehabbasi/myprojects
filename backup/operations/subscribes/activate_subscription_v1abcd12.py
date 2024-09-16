from datetime import datetime

from django.conf import settings

from AppBase.usage import usage
from Business.models import Subscription, Business


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
def activate_subscription_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            subscription = Subscription.g(key__exact=d['key'], service__provider__customer__exact=customer)
            _ = subscription.key

            state = d["action"]
            validate_state = state in [True, False]

            if not validate_state:
                raise ValueError
        except (ValueError, KeyError, AttributeError):
            return 400
    if 'Save':
        subscription.available = state
        subscription.save()

    return subscription.api(customer)
