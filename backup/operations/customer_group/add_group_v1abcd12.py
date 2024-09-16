from Business.models import CustomerGroup


def add_group_v1abcd12(req, d, device):
    if 'add customer group':
        try:
            title = d['title']

            title_validate = title and len(title) > 3
            if not title_validate:
                raise Exception

        except ValueError:
            return 401

        customer_group = CustomerGroup(title=title)
        customer_group.save()

        return 200
