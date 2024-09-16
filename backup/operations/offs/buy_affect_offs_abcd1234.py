from Business.models import Off
from Business.operations.offs.calculate_order_off_data_abcd123 import calculate_order_off_data_abcd1234


def buy_affect_offs_abcd1234(cache, business, customer, off_code):
    not_certain_offs = []
    config = business.subscription.config['features']

    if "For Products" and config['products']:
        for each in cache.data['order']['products']:
            available_offs = Off.f(business__exact=business, for_certain_products__key__exact=each['key'])
            each = calculate_order_off_data_abcd1234(
                each=each,
                customer=customer,
                business=business,
                available_offs=available_offs,
                off_code=off_code if off_code else None
            )
            not_certain_offs += [x.key for x in available_offs]

    if "For Services" and config['subscriptions']:
        for each in cache.data['order']['services']:
            available_offs = Off.f(
                business__exact=business,
                for_certain_services__key__exact=each['key']
            )

            each = calculate_order_off_data_abcd1234(
                each=each,
                customer=customer,
                business=business,
                available_offs=available_offs,
                off_code=off_code if off_code else None
            )
            not_certain_offs += [x.key for x in available_offs]

    if "For General":
        available_offs = Off.f(business__exact=business).exclude(key__in=not_certain_offs)
        general = calculate_order_off_data_abcd1234(
            each=cache.data['order']['general_off'],
            customer=customer,
            business=business,
            available_offs=available_offs,
            off_code=off_code if off_code else None
        )

    if "Distribute the General Off Between Transactions" and general['off'] > 0:
        if "For Products and Services":
            for each in cache.data['order']['products'] + cache.data['order']['services']:
                if_general_off = general['off'] * each['general_off_stake']
                if if_general_off > each['off']:
                    each['off'] = if_general_off
                    each['off_data'] = {
                        "key": general['off_data']['key'],
                        "amount": if_general_off,
                        "count": each['count'],
                        "affect_type": general['off_data']['affect_type'],
                        "title": general['off_data']['title'],
                        "code": general['off_data']['code'] if 'code' in general['off_data'].keys() else None
                    }

    additional_discount = cache.data["order"]["additional_discount"]
    if "Distribute the Additional Discount Between Transactions" and additional_discount['amount'] > 0:
        if "For Products and Services":
            for each in cache.data['order']['products'] + cache.data['order']['services']:
                each['off'] += additional_discount['amount'] * each['general_off_stake']

    return cache
