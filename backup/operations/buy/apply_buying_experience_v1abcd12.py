from datetime import datetime, timedelta

import jdatetime

from AppBase.usage import usage
from Business.models import Business, BusinessProduct, SubscriptionService
from Business.models import SubscriptionServiceCostModel, Order
from Business.operations.offs.buy_affect_offs_abcd1234 import buy_affect_offs_abcd1234
from Platform.models import Cache, iTransaction, Metadata
from toolkit import convert_to_j_date


@usage
def apply_buying_experience_v1abcd12(_, d, device):
    if "Validate Request and Initialize":
        try:
            cache = Cache.g(token__exact=d['key']) if 'key' in d.keys() and d['key'] else None
            business = Business.k(d['business_key'] if 'business_key' in d.keys() else None)
            cancel = d['cancel'] if 'cancel' in d.keys() else False

            delivered_order = d['delivered_order'] if 'delivered_order' in d.keys() else False
            renew_order = d['renew_order'] if 'renew_order' in d.keys() else False
            close_order = d['close_order'] if 'close_order' in d.keys() else False

            if renew_order:
                cache = Order.find_cache(renew_order)
                if not cache:
                    return 404

                business = Business.k(cache.business_ilink)

            try:
                config = business.subscription.config['features']
            except (AttributeError, TypeError):
                config = None

            if "Check For Preparing Time":
                time_to_ready = d['time_to_ready'] if 'time_to_ready' in d.keys() else False

            if "Additional Amount and Discount":
                additional_amount = None
                config_additional_amount = config['additionalAmount']
                if "additional_amount" in d.keys() and d['additional_amount'] != '' and config_additional_amount:
                    additional_amount = float(d["additional_amount"])

                additional_discount = None
                config_additional_discount = config['additionalDiscount']
                if "additional_discount" in d.keys() and d['additional_discount'] != "" and config_additional_discount:
                    additional_discount = float(d["additional_discount"])

            off_code = d['code'] if "code" in d.keys() else False

            validate = cache or business
            if not validate:
                raise ValueError

            try:
                store_config = business.subscription.config
            except (AttributeError, TypeError):
                store_config = None

        except (KeyError, ValueError, AttributeError):
            return 400

    if "Initialize Cache":
        if not cache:
            cache = Cache.buying_experience(business_key=business.key, device=device)

    if "Verification of Request":
        role = None
        if not device or device.user.key != business.customer.key:
            role = 'buyer'

        if device and device.user.key == business.customer.key:
            role = 'business'
            if not cache:
                return 401

        if not role:
            return 401

        if role == 'business' and cache.expire_time < datetime.now():
            if renew_order and (cache.create - datetime.now()).days <= 1:
                cache.expire_time = datetime.now() + timedelta(minutes=1)

            else:
                return 404  # @todo must check

        if 'state' in cache.data.keys() and cache.data['state'] == 'paid':
            return 401

        if 'cancel' in cache.data.keys() and cache.data['cancel']:
            return 401

        if "Cancel Order" and cancel:
            cache.data['cancel'] = True
            cache.trashed = True
            cache.save()
            return cache.data

        if "Check For Delivered Orders" and delivered_order:
            cache.data['state'] = 'delivered'
            if 'renew_order' in cache.data.keys():
                del cache.data['renew_order']

            cache.trashed = True
            cache.save()
            return cache.data

        if "Preparing Time To Ready" and role == 'business':
            if time_to_ready:  # Business enter new time to ready
                cache.data['time_to_ready'] = time_to_ready
                cache.data['delivery_timestamp'] = datetime.now().timestamp() + int(time_to_ready) * 60

    if "Update Cache products and services according to request products":
        if "products" in d.keys() and config["products"]:
            cache.data["products"].update(d["products"])
            for product_key, count in d['products'].items():
                if not count or count <= 0:
                    del cache.data["products"][product_key]
                    continue

                product = BusinessProduct.k(product_key)
                if not product or not product.available or (type(product.stock) == int and product.stock <= 0):
                    del cache.data["products"][product.key]
                    continue

                if product.stock and product.stock < int(count):
                    cache.data['products'][product_key] = product.stock

        if "services" in d.keys() and config['subscriptions']:
            cache.data["services"].update(d["services"])
            for service_key, cost_model_key in d['services'].items():
                if cost_model_key == '':
                    try:
                        del cache.data["services"][service_key]
                    except KeyError:
                        pass

                cost_model = SubscriptionServiceCostModel.k(cost_model_key)
                if not cost_model:
                    continue

    if "Initialize Order":
        cache.data['order'] = {
            "additional_amount": 0,
            "additional_discount": 0,
            "products": [],
            "services": [],
            'general': {},
            "amount": 0,
            "off": 0
        }

        if 'Check Products' and config['products']:
            for product_key, count in cache.data['products'].items():
                product = BusinessProduct.k(product_key)
                cache.data['order']['products'].append({
                    "key": product_key,
                    "count": count,
                    "base_price": product.price,
                    "amount": count * product.price,
                    "off": 0,
                    "off_data": {},
                    "commission": 0
                })

        if 'Check Services' and config['subscriptions']:
            for service_key, cost_model_key in cache.data['services'].items():
                cost_model = SubscriptionServiceCostModel.k(cost_model_key)

                cache.data['order']['services'].append({
                    "key": service_key,
                    "cost_model_key": cost_model_key,
                    "base_price": cost_model.cost,
                    "amount": cost_model.cost,
                    "count": 1,
                    "off": 0,
                    "off_data": {},
                    "commission": 0
                })

        if 'Check for Additional Amount' and config['additionalAmount'] and additional_amount:
            cache.data['additional_amount'] = additional_amount

        if 'Check for Additional Discount' and config['additionalDiscount'] and additional_discount:
            cache.data['additional_discount'] = additional_discount

        if 'Check for Off Code' and off_code:
            cache.data["code"] = off_code

        cache.calculate_total_amount(business.subscription.config)

    if "Verify Order Items Availability":
        if "Check Products" and config['products']:
            for each in cache.data['order']['products']:
                product = BusinessProduct.k(each['key'])
                if product.stock is not None and product.stock < each["count"]:
                    each["count"] = product.stock  # @todo should display a message to customer

                if product.business_ilink != business.key:
                    return 401

        if "Check Services" and config['subscriptions']:
            for each in cache.data['order']['services']:
                cost_model = SubscriptionServiceCostModel.k(each['cost_model_key'])
                service = SubscriptionService.k(each['key'])

                if cost_model.service.key != service.key:
                    return 401

                if service.provider.key != business.key:
                    return 401

    if "Initialize Offs" and config['offs']:
        cache.data['order']['manual']['base_price'] = cache.data['order']["amount"]  # for general offs
        cache = buy_affect_offs_abcd1234(
            cache=cache,
            business=business,
            customer=None,
            off_code=cache.data["code"] if 'code' in cache.data.keys() else None
        )
        cache.calculate_total_amount(store_config)

    if "Business Supports Turn" and config["turn"] and not cache.data["turn_number"]:
        meta = Metadata.k('business_' + business.key + '_last_order_id')
        turn_number = int(meta.value) if int(meta.value) > 0 else int(meta.value) + 1

        four_am = jdatetime.datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)
        if convert_to_j_date(meta.update) <= four_am < convert_to_j_date(datetime.now()):
            turn_number = 1

        cache.data["turn_number"] = turn_number
        business.customer.meta_update('business_' + business.key + '_last_order_id', turn_number + 1)

    if close_order and cache.data['paid'] >= cache.data['amount']:
        if config['waitingAfterPayment']:
            cache.data['state'] = 'waiting'
        else:
            cache.data['state'] = 'paid'
            cache.expire_time = datetime.now()

    if "Check For Loyal Customer":
        if device and role == 'buyer':
            transactions = iTransaction.f(dst__exact=business.customer, src__exact=device.user,
                                          trans_type__in=['product', 'subscription', 'manual']).count()

            cache.data["purchase_number"] = transactions + 1

        if not device:
            cache.data["purchase_number"] = 1

    if "He Is Customer":
        if role == "buyer":
            cache.expire_time = datetime.now() + timedelta(minutes=1)
            cache.save()

            customer_response = {
                "test": cache.data,
                "key": cache.data["key"],
                "token": cache.data["token"],
                "state": cache.data["state"],
                "cancel": cache.data["cancel"],

                "off": cache.data["order"]["off"],
                "code": cache.data["code"],
                "amount": cache.data['order']["amount"],
                "paid": cache.data['paid'],

                "products": cache.data["products"],
                "services": cache.data["services"],
                "additional_discount": cache.data['order']['additional_discount']['amount'],
                "additional_amount": cache.data['order']['manual']['amount'],
                "turn_number": cache.data["turn_number"],
                "purchase_number": cache.data["purchase_number"]
            }

            if 'time_to_ready' in cache.data.keys():
                customer_response.update({
                    'time_to_ready': cache.data['time_to_ready'],
                    "delivery_timestamp": cache.data['delivery_timestamp']
                })

            return customer_response

    if "He Is Business Owner":
        if cache.device:
            customer_info = cache.device.user.api()
        else:
            customer_info = {
                "username": "guest",
                "fullname": "کاربر میهمان",
                "profile": 'https://s.virdaar.ir/person_profile_default.png'  # @todo random pictures
            }

        products = cache.data['order']['products']
        services = cache.data['order']['services']
        product_offs = {'product-' + x['key']: x['off_data'] for x in products if 'off_data' in x.keys()}
        service_offs = {'subscription-' + x['key']: x['off_data'] for x in services if 'off_data' in x.keys()}
        # general_off =[] #@todo check general offs

        if "Preparing Waiting Products":
            waiting_products = {}
            caches = Cache.f(business_ilink__exact=business.key)
            products = [cache.data['products'] for cache in caches if
                        cache.data['state'] == 'waiting' and cache.data['products']]

            for product_data in products:
                for key, value in product_data.items():
                    if key not in waiting_products:
                        waiting_products.update({key: value})

                    waiting_products[key] += value

        cache.save()
        business_response = {
            "key": cache.data["key"],
            "token": cache.data["token"],
            "state": cache.data["state"],
            "cancel": cache.data["cancel"],

            "off": cache.data["order"]["off"],
            "off_data": {**product_offs, **service_offs},
            "code": cache.data["code"],
            "amount": cache.data['order']["amount"],
            "paid": cache.data['paid'],
            "products": cache.data["products"],
            "services": cache.data["services"],
            "additional_discount": cache.data['order']['additional_discount']['amount'],
            "additional_amount": cache.data['order']['manual']['amount'],
            # "additional_amount": cache.data["order"]["additional_amount"],
            "waiting_products": waiting_products,

            "turn_number": cache.data["turn_number"],
            "purchase_number": cache.data["purchase_number"],

            'customer': customer_info
        }

        if 'time_to_ready' in cache.data.keys():
            business_response.update({
                'time_to_ready': time_to_ready,
                "delivery_timestamp": cache.data['delivery_timestamp']
            })

        return business_response
