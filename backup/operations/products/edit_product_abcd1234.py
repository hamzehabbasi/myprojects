from datetime import timedelta, datetime

import jdatetime
from django.db.models import Sum

from AppBase.usage import usage
from Business.models import BusinessProduct, iTSubscription
from Business.models import BusinessProductLabel
from Business.text import *
from toolkit import convert_to_j_date
from toolkit import image_base64_upload


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
def edit_product_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
            product = BusinessProduct.g(key__exact=d['product_key'], business__customer__exact=customer)
            business = product.business

            name = d['name']
            image = d['image'] if 'image' in d.keys() else None
            price = float(d['price'])
            unit = d['unit']
            description = d['description'] if 'description' in d.keys() else ''

            try:
                stock = int(d['stock'])
            except (ValueError, KeyError, TypeError):
                stock = None

            try:
                cost = float(d['cost'])
            except (ValueError, KeyError, TypeError):
                cost = 0

            try:
                preparing_time = int(d['preparing_time'])
            except (ValueError, KeyError, TypeError):
                preparing_time = 0

            validate = len(name) > 2 and len(unit) > 0 and price > 0
            if not validate:
                raise Exception

            labels = []
            if 'labels' in d.keys():
                labels = BusinessProductLabel.f(key__in=d['labels'], business__exact=business)

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Check for New Image':
        if image and not image.startswith("https"):
            if 'Clean Previous Image' and product.image and product.image.url.startswith("https"):
                product.image.delete(save=True)

            if 'Upload New Image':
                if image:
                    image_name, image_data = image_base64_upload(image)
                    product.image.save(image_name, image_data)

    if "Delete Previous Image":
        if not image and product.image and product.image.url.startswith("https"):
            product.image.delete(save=True)

    if 'Clean Previous Labels':
        product.labels.clear()

    if 'Save Product':
        product.name = name
        product.price = price
        product.stock = stock
        product.unit = unit
        product.description = description
        product.preparing_time = preparing_time
        product.cost = cost
        product.save()

    if 'Save Labels':
        for label in labels:
            product.labels.add(label)

    return product.seller_api_v1()
