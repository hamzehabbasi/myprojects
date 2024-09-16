from datetime import datetime

import jdatetime

from AppBase.usage import usage
from Business.models import Off, BusinessProduct, CustomerGroup, \
    VitrineCategory, SubscriptionService


def seller_api_v1(self):
    items = self.for_certain_products.A()
    for_certain_products = [x.key for x in items] if items.count() > 0 else None

    items = self.for_certain_services.A()
    for_certain_services = [x.key for x in items] if items.count() > 0 else None

    items = self.for_certain_categories.A()
    for_certain_categories = [x.key for x in items] if items.count() > 0 else None

    items = self.for_certain_customer_groups.A()
    for_certain_customer_groups = [x.key for x in items] if items.count() > 0 else None

    items = self.for_certain_customers.A()
    for_certain_customers = [x.key for x in items] if items.count() > 0 else None

    return {
        'key': self.key,
        'off_type': self.off_type,
        'affect_type': self.affect_type,
        "expire_date": self.expire_date.timestamp() if self.expire_date else False,
        "code": self.code,
        "business_key": self.business.key,
        "off_amount": self.off_amount,
        "total_sell": self.amount_consumed,
        "off_budget_consumed": self.off_budget_consumed,
        "off_budget": self.off_budget,
        "upto_certain_sell_amount": self.upto_certain_sell_amount,
        "upto_certain_sell_amount_consumed": self.amount_consumed,
        "upto_certain_sell_count": self.upto_certain_sell_count,
        "upto_certain_sell_count_consumed": self.count_consumed,
        "for_more_than_amount": self.for_more_than_amount,

        "for_continuous_subscription_base_duration": self.for_continuous_subscription_base_duration,
        "for_continuous_subscription": self.for_continuous_subscription,

        "for_certain_categories": for_certain_categories,
        "for_certain_customer_groups": for_certain_customer_groups,
        "for_certain_customers": for_certain_customers,
        "for_certain_products": for_certain_products,
        "for_certain_services": for_certain_services,

        "count": self.count,

        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed,

    }


@usage
def add_off_v1abcd12(req, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
        except AttributeError:
            return 401

        try:
            business = customer.businesses.g(key__exact=d['business_key'])

            code = None
            if d['code'] and d['code'] != "":
                code = d['code'].upper()

            upto_certain_sell_count = None
            if d['upto_certain_sell_count'] and d['upto_certain_sell_count'] != "":
                upto_certain_sell_count = int(d['upto_certain_sell_count'])

            off_budget = None
            if d['off_budget'] and d['off_budget'] != "":
                off_budget = float(d['off_budget'])
            else:
                off_budget = 1000  # @todo must remove after fix it @front

            upto_certain_sell_amount = None
            if d['upto_certain_sell_amount'] and d['upto_certain_sell_amount'] != "":
                upto_certain_sell_amount = int(d['upto_certain_sell_amount'])

            expire_date = None
            if d['expire_date'] and d['expire_date'] != "":
                expire_date = d['expire_date']

            for_more_than_amount = None
            if d['for_more_than_amount'] and d['for_more_than_amount'] != "":
                for_more_than_amount = d['for_more_than_amount']

            for_continuous_subscription_base_duration = None
            if d['for_continuous_subscription_base_duration'] and d['for_continuous_subscription_base_duration'] != "":
                for_continuous_subscription_base_duration = d['for_continuous_subscription_base_duration']

            for_continuous_subscription_service = None
            if d['for_continuous_subscription_service'] and d['for_continuous_subscription_service'] != "":
                for_continuous_subscription_service = d['for_continuous_subscription_service']

            for_certain_customer_groups = None
            if d['for_certain_customer_groups'] and d['for_certain_customer_groups'] != "":
                for_certain_customer_groups = d['for_certain_customer_groups']

            for_certain_services = None
            if d['for_certain_services'] and d['for_certain_services'] != "":
                for_certain_services = d['for_certain_services']

            for_certain_products = None
            if d['for_certain_products'] and d['for_certain_products'] != "":
                for_certain_products = d['for_certain_products']

            off_type = d['off_type']
            off_amount = float(d['off_amount'])

            for_certain_categories = False
            if d['for_certain_categories'] and d['for_certain_categories'] != "":
                for_certain_categories = d['for_certain_categories']

            config = business.subscription.config

            if code and len(code) < 4:
                raise Exception

        except (ValueError, KeyError, AttributeError):
            return 400

    if "Check For Off Access" and not config['features']['offs']:
        return 401

    if "Verification User and Business":
        business_owner = business.customer
        if business_owner.key != customer.key:
            return 401

    off = Off(
        off_amount=off_amount,
        off_type=off_type,
        business=business
    )
    off.save()

    if "Check For Expire Date" and expire_date and config['features']['offDate']:
        split_license_date = expire_date.split("/")
        date = jdatetime.date(day=int(split_license_date[2]), month=int(split_license_date[1]),
                              year=int(split_license_date[0]))

        date = date.togregorian()
        off.expire_date = datetime.combine(date, datetime.min.time())

    if "Check For Discount CODE" and code and config['features']['offDiscountCode']:
        off.code = code

    if "Check For Off Budget" and off_budget and config['features']['offBudget']:
        off.off_budget = off_budget

    if "Check For Off Upto Certain Amount" and upto_certain_sell_amount and config['features']['offUptoCertainAmount']:
        off.upto_certain_sell_amount = upto_certain_sell_amount

    if "Check For Off Upto Certain Count" and upto_certain_sell_count and config['features']['offUptoCertainCount']:
        off.upto_certain_sell_count = upto_certain_sell_count

    if "Check For Off More Than Amount" and for_more_than_amount and config['features']['offMoreThanAmount']:
        off.for_more_than_amount = for_more_than_amount

    if "Check For Off Certain Products" and for_certain_products and config['features']['offSpecificProducts']:
        products = BusinessProduct.f(key__in=for_certain_products)
        off.for_certain_products.add(*products)

    if "Check For Off Certain Services" and for_certain_services and config['features']['offSpecificServices']:
        subscriptions = SubscriptionService.f(key__in=for_certain_services)
        off.for_certain_services.add(*subscriptions)

    if "Check For Off Continuous Subscribes" and config['features']['offContinuousSubscribes']:
        if for_continuous_subscription_service and for_continuous_subscription_base_duration:
            off.for_continuous_subscription_service = for_continuous_subscription_service
            off.for_continuous_subscription_base_duration = for_continuous_subscription_base_duration

    off.save()

    if " Check For Category Key" and for_certain_categories and config['features']['offCategory']:
        current_category = VitrineCategory.f(key__in=for_certain_categories)
        for category in current_category:
            off.for_certain_categories.add(category)

    if "Customer Group" and for_certain_customer_groups and config['features']['offCustomerGroup']:
        for key in for_certain_customer_groups:
            customer_group = CustomerGroup.k(key)
            if not customer_group:
                continue

            off.for_certain_customer_groups.add(customer_group)

    return 200, off.seller_api_v1()
