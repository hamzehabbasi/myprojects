from Business.models import CustomerGroup
from Platform.models import User


def add_customer_to_group_v1abcd12(req, d, device):
    if 'add customer to group':
        try:
            group_key = d['group key']
            customers_keys = d['customers keys']

            group = CustomerGroup.k(group_key)
            if not group:
                raise Exception

            for item in customers_keys:
                customer = User.k(item)
                if not customer:
                    raise Exception

        except KeyError:
            return 401

        for item in customers_keys:
            customer = User.k(item)
            group.customer.add(customer)
        group.save()
        return 200
