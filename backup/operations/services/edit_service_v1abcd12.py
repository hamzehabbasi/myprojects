from datetime import timedelta, datetime

import jdatetime
from django.db.models import Sum

from AppBase.usage import usage
from Business.models import SubscriptionService, SubscriptionServiceCostModel, iTSubscription
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
def edit_service_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
            service = SubscriptionService.g(key__exact=d['service_key'], provider__customer__exact=customer)
            _ = service.provider

            title = d['title']
            cost_models = d['cost_models']

            image = d['image'] if 'image' in d.keys() else None
            description = d['description'] if 'description' in d.keys() else ''

            validate_title = type(title) is str and len(title) > 3
            validate_cost_models = type(cost_models) is list and len(cost_models) > 0
            validate = validate_title and validate_cost_models

            if not validate:
                raise ValueError

            cost_model_keys = [x["key"] for x in d['cost_models']]
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Verify Ownership of Cost Models':
        requested = SubscriptionServiceCostModel.af(key__in=cost_model_keys)
        for each in requested:
            if each.service.key != service.key:
                return 400

    if 'Check for New Image':
        if image and not image.startswith("https"):
            if 'Clean Previous Image' and service.image and service.image.url.startswith("https"):
                service.image.delete(save=True)

            if 'Upload New Image':
                if image:
                    image_name, image_data = image_base64_upload(image)
                    service.image.save(image_name, image_data)

    if "Delete Previous Image":
        if not image and service.image and service.image.url.startswith("https"):
            service.image.delete(save=True)

    if 'Save Service':
        service.title = title
        service.description = description
        service.save()

    if 'Create Cost Models Memory and Trash them all':
        cost_models_memory = {}
        for each in service.cost_models.all():
            each.trashed = True
            cost_models_memory[each.key] = each

    if 'Save New Cost Models and Trash out previous items':
        for cost_model in cost_models:
            key = cost_model["key"]
            if key not in cost_models_memory.keys():
                cost_models_memory[key] = SubscriptionServiceCostModel(service=service)
                cost_models_memory[key].save()

            cost_models_memory[key].interval = cost_model['interval']
            cost_models_memory[key].cost = cost_model['cost']
            cost_models_memory[key].title = cost_model['title']
            cost_models_memory[key].trashed = False

        SubscriptionServiceCostModel.objects.bulk_update(
            cost_models_memory.values(),
            fields=['trashed', 'title', 'interval', 'cost']
        )

    return service.seller_api_v1()
