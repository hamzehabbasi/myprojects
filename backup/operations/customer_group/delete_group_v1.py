from Business.models import CustomerGroup


def delete_group_v1abcd12(req, d, device):
    if 'Delete group or groups':
        try:
            groups_keys = d['group key']

            for key in groups_keys:
                group = CustomerGroup.k(key)
                if not group:
                    raise Exception

        except KeyError:
            return 401

        for key in groups_keys:
            group = CustomerGroup.k(key)
            group.trashed = True
            group.save()
        return 200
