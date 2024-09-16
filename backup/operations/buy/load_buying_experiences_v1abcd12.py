from datetime import datetime, timedelta

from AppBase.usage import usage
from Business.models import Business
from Platform.models import Cache


@usage
def load_buying_experiences_v1abcd12(_, __, device):
    customer = device.user

    if 'Customer Owns Which Businesses':
        businesses = [x.key for x in customer.businesses.A()]

    if 'Fetch Active Customers in Stores of customer':
        customers = []
        caches = Cache.f(business_ilink__in=businesses, update__gte=datetime.now() - timedelta(minutes=1))
        for cache in caches.order_by('-update'):
            if cache.data['state'] in ['delivered', 'paid']:
                continue

            if cache.data['cancel']:
                continue

            # if cache.data['role'] == 'business':
            #     continue
            business = Business.k(cache.business_ilink)
            cafe_pic = 'https://s.virdaar.ir/person_profile_default.png'
            restaurant_pic = 'https://s.virdaar.ir/icon-user-wight.jpg'
            customer_info = cache.device.user.api() if cache.device else {
                "fullname": "کاربر میهمان",
                "profile": ''
            }
            if not customer_info['profile']:
                customer_info['profile'] = cafe_pic if business.business_type == 'cafe' else restaurant_pic

            customers.append({
                "key": cache.token,
                "business_key": cache.business_ilink,
                "create": cache.create.timestamp(),
                "update": cache.update.timestamp(),
                "customer": customer_info,
                "state": cache.data['state']
            })

    # if len(customers) == 0:  # clean flag of buying experience for preventing over load
    #     customer.meta_update('buying_experiences_update', '0') @TODO should check this

    return sorted(customers, key=lambda x: x["create"])
