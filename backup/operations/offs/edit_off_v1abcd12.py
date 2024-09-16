from datetime import timedelta, datetime

import jdatetime
from django.db.models import Sum

from AppBase.usage import usage
from Business.models import Off, BusinessProduct, VitrineCategory, SubscriptionService, iTSubscription
from Business.text import *
from toolkit import convert_to_j_date


def seller_api_v1(self):
    now = jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    year_ago = now.togregorian() - timedelta(days=365)
    month_ago = now.togregorian() - timedelta(days=30)
    week_ago = now.togregorian() - timedelta(days=7)
    subscriptions = self.service_subscriptions.A()
    sells = iTSubscription.f(subscription__in=subscriptions).select_related('transaction')

    daily_trends = {}
    monthly_trends = {}
    weekly_trends = {}

    for sell in sells:
        off_amount = sell.transaction.it_off.off_amount if sell.transaction.it_off else 0
        amount = (sell.base_price - off_amount)

        if "Not In Recent Year" and sell.create < year_ago:
            continue

        if "In Recent Month" and datetime.now() >= sell.create > month_ago:
            day_id = f"{sell.create.year}{sell.create.month}{sell.create.day}"

            if day_id not in daily_trends.keys():
                j = convert_to_j_date(sell.create)
                day_label = f"{j.day} {j.j_months_fa[j.month - 1]} {j.year}"

                daily_trends[day_id] = {
                    "date": sell.create.timestamp(),
                    "date_string": f'{j.year}/{j.month}/{j.day}',
                    "label": day_label,
                    "sell_count": 0,
                    "sell_amount": 0
                }

            daily_trends[day_id]["sell_amount"] += amount
            daily_trends[day_id]["sell_count"] += 1

        if "Monthly Trends":
            month_id = f"{sell.create.year}{sell.create.month}"

            if month_id not in monthly_trends.keys():
                j = convert_to_j_date(sell.create)
                month_label = f"{j.j_weekdays_fa[j.weekday()]}"

                monthly_trends[month_id] = {
                    "date": sell.create.timestamp(),
                    "label": month_label,
                    "sell_count": 0,
                    "sell_amount": 0
                }

            monthly_trends[month_id]["sell_amount"] += amount
            monthly_trends[month_id]["sell_count"] += 1

        if "Weekly Trends" and datetime.now() >= sell.create > week_ago:
            week_number = sell.create.strftime("%V")
            week_id = f"{week_number}{sell.create.weekday()}"
            if week_id not in weekly_trends.keys():
                j = convert_to_j_date(sell.create)
                week_label = f"{j.j_weekdays_fa[j.weekday()]}"

                weekly_trends[week_id] = {
                    "date": sell.create.timestamp(),
                    "label": week_label,
                    "sell_count": 0,
                    "sell_amount": 0
                }

            weekly_trends[week_id]["sell_amount"] += amount
            weekly_trends[week_id]["sell_count"] += 1

    total_price = sells.aggregate(Sum('base_price'))['base_price__sum'] if len(sells) > 0 else 0
    total_off = sum([(s.transaction.it_off.off_amount if s.transaction.it_off else 0) for s in sells])
    return {
        "key": self.key,
        "title": self.title,
        "provider": {
            'title': self.provider.title,
            'logo': self.provider.logo.url if self.provider.logo else False,
            'key': self.provider.key
        },
        "description": self.description,
        "image": (settings.VIRDAAR_ENDPOINT_URL + self.image.name) if self.image else False,
        "cost_models": [x.api_v1() for x in self.cost_models.A().order_by('-cost')],
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed,
        "total_sell_amount": total_price - total_off,
        "total_sell_count": len(sells),
        "total_off": total_off,
        "daily_trends": daily_trends,
        "weekly_trends": weekly_trends,
        "monthly_trends": monthly_trends,
        "order": self.order,
        "available": self.activate
    }


@usage
def edit_off_v1abcd12(req, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
        except AttributeError:
            return 401

        try:
            off = Off.g(key__exact=d['key'], business__customer__exact=customer)
            business = off.business

            code = None
            if d['code'] and d['code'] != "":
                code = d['code'].upper()

            upto_certain_sell_count = None
            if d['upto_certain_sell_count'] and d['upto_certain_sell_count'] != "":
                upto_certain_sell_count = int(d['upto_certain_sell_count'])

            off_budget = None
            if d['off_budget'] and d['off_budget'] != "":
                off_budget = float(d['off_budget'])

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

            config = business.subscription.config

            for_certain_categories = False
            if d['for_certain_categories'] and d['for_certain_categories'] != "":
                for_certain_categories = d['for_certain_categories']

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

    if "Set UP New Amount":
        off.off_amount = off_amount
        off.off_type = off_type

    if "Check For Expire Date" and expire_date and config['features']['offDate']:
        split_license_date = expire_date.split("/")
        off.expire_date = jdatetime.date(
            day=int(split_license_date[2]),
            month=int(split_license_date[1]),
            year=int(split_license_date[0]),
            hour=23, minute=59, second=59
        ).togregorian()

    if "Check For Discount CODE" and config['features']['offDiscountCode']:
        if not off.off_budget_consumed:
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

    if " Check For Category Key" and for_certain_categories and config['features']['offCategory']:
        current_category = VitrineCategory.f(key__in=for_certain_categories)
        for category in current_category:
            off.for_certain_categories.add(category)

    if "Customer Group" and for_certain_customer_groups and config['features']['offCustomerGroup']:
        for group in off.for_certain_customer_groups.A():
            off.delete(group)

    off.save()

    return off.seller_api_v1()
