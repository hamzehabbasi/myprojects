from datetime import datetime

from AppBase.usage import usage


@usage
def delete_business_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
            business = customer.businesses.k(d['business_key'])
            if not business:
                customer.save_synchronize_flag('businesses', customer.pk)
                return 200

        except (ValueError, KeyError, AttributeError):
            return 400

    if "Check for Active Subscriptions":
        services = business.subscription_services.A()
        total = 0
        for service in services:
            subscriptions = service.service_subscriptions.A()
            if subscriptions:
                total += len(subscriptions)
        if total > 0:
            return 405

    if "Delete Services":
        for service in services:
            service.cost_models.A().update(trashed=True)

        business.subscription_services.A().update(trashed=True)

    if "Delete Subscription":
        subscription = business.subscription
        subscription.expire = datetime.now()
        subscription.save()

    if "Delete Business":
        business.trashed = True
        business.save()

    return 200
