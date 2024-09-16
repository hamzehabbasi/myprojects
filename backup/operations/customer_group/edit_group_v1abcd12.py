from Business.models import CustomerGroup, SubscriptionService
from Platform.models import User


def edit_group_v1abcd12(req, d, device):
    if 'Edit group':
        try:
            group_key = d['group key']
            title = d['title']
            customers_keys = d['customers keys']
            subscription_service_key = d['subscription service']

            group = CustomerGroup.k(group_key)
            if not group:
                raise Exception

            subscription_service = SubscriptionService.k(subscription_service_key)
            if not subscription_service:
                pass

        except KeyError:
            return 401

        group.title = title

        for item in customers_keys:
            customer = User.k(item)
            group.customers.add(customer)

        group.subscription_service = subscription_service

        group.save()
        return 200
