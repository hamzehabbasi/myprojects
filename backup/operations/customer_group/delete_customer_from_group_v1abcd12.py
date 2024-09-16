from Business.models import CustomerGroup
from Platform.models import User


def delete_customer_from_group_v1abcd12(req, d, device):
    if 'Delete number of customer from group':
        try:
            customers_keys = d['customer keys']
            group_key = d['group key']

            group = CustomerGroup.k(group_key)
            if not group:
                raise Exception

            for item in customers_keys:
                customer = User.k(item)
                if not customer:
                    raise Exception

        except ValueError:
            return 401

        for item in customers_keys:
            customer = User.k(item)
            group.customers.remove(customer)
        group.save()
        return 200
