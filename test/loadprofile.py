# import copy
# from datetime import datetime, timedelta
#
# from django.conf import settings
# from django.db.models import Sum, DateTimeField
# from django.db.models.functions import Trunc
#
# from AppBase.usage import usage
# from Business.text import GROUP_REQUIREMENTS_DETAILS
# from Platform.models import User, iTransaction, iTGift
# from toolkit import find_weeks_v2
# from .models import Program, Assign, Permission
#
#
# def customer_api(self):
#     response = {
#         "key": self.key,
#         "total_amount": self.amount,
#         "create": self.create.timestamp(),
#         "expire": self.expire.timestamp() if self.expire else False,
#         "description": self.description,
#         "link": self.config['url'] if 'url' in self.config.keys() else None,
#         "products": [],
#         "services": [],
#         "businesses": {},
#     }
#
#
# def self_api(self, more_fields=None):
#     if more_fields is None:
#         more_fields = []
#
#     fields = ["fullname", "profile"] + more_fields
#
#     response = {
#         "username": self.username,
#         "taxi": {}
#     }
#     information = self.information
#
#     for x in fields:
#         try:
#             response[x] = information[x]
#         except KeyError:
#             response[x] = None
#
#     return response
#
#
# def program_api(program):
#     return {
#         "name": program.name,
#         "key": program.key,
#         "permissions": [permission.key for permission in program.permissions.all()]
#     }
#
#
# @usage
# def load_profiles_v4(request):
#     try:
#         me = request.DEVICE.user
#     except AttributeError:
#         return 401
#     try:
#         keys = request.data['keys']
#     except (KeyError, AttributeError, TypeError):
#         keys = None
#
#     profiles = []
#
#     if 'My Profile' and (not keys or 'self' in keys):
#         virsa = me.assets.g(plan_ilink__exact=settings.VIRSA_PLAN_KEY)
#         virdo = me.assets.g(plan_ilink__exact=settings.VIRDO_PLAN_KEY)
#         virdo_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRDO_PLAN_KEY)
#         virsa_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRSA_PLAN_KEY)
#         virdaar_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRDAR_PLAN_KEY)
#
#         gifts = iTGift.f(expire__gt=datetime.now())
#
#         self = {
#             **self_api(me, more_fields=['mobile', 'email', 'shaparak_payout', 'shaparak_cash']),
#             **{
#                 "virsa": virsa.count if virsa else 0,
#                 "virdo": virdo.count if virdo else 0,
#                 "virdo_old": virdo_old.count if virdo_old else 0,
#                 "virsa_old": virsa_old.count if virsa_old else 0,
#                 "virdaar_old": virdaar_old.count if virdaar_old else 0,
#
#                 "magic_charge": float(me.magic_charge_rate),
#                 "blocked_cash": sum([x.amount for x in iTransaction.f(trans_type__exact='blocked', src__exact=me)]),
#                 "key": "self",
#                 "identifier": me.identifier,
#                 "create": me.create.timestamp(),
#                 "update": me.update.timestamp(),
#                 "labels": [],
#                 "beta": {
#                     "join": me.meta('beta-program-enrollment'),
#                     "expire": me.meta('beta-program-expired')
#                 },
#                 "ux": {}
#             }
#         }
#
#         transactions = iTransaction.f_or(src__exact=me, dst__exact=me)
#
#         if "Check for Limited Bill User" and transactions.count() >= 15:
#             self["labels"].append("charity")
#             self["labels"].append("pay_bill")
#             self["labels"].append("pay_consumption")
#             self["labels"].append("transfer_money")
#
#         if "Check for Blocked User":
#             if me.status == 'blocked':
#                 self["labels"].append("blocked")
#
#         if "Check for Limited User":
#             if me.status == 'limited':
#                 self["labels"].append("limited")
#
#         if "Check for Venture Customer":
#             is_venture_customer = transactions.f(trans_type__in=['unit', 'gift_unit', 'unit_transaction']).count() > 0
#             if is_venture_customer:
#                 self["labels"].append("venture")
#
#         if "Check for Business Customer":
#             business_stack = me.businesses.A()
#             business_uses = business_stack.count()
#
#             if business_uses > 0:
#                 self["labels"].append("business")
#
#             if business_uses > 1:
#                 self["labels"].append("multi_business")
#
#             if business_uses == 1:
#                 self["ux"]["business"] = business_stack[0].brand
#
#         if "Monirs Squad":
#             if 'charity' not in self["labels"] or 'transfer' not in self["labels"]:
#                 identifier = User.k(me.meta('identifier'))
#                 if identifier:
#                     monirs_squad = list(set(iTransaction.f(
#                         src_id__exact=28,
#                         trans_type__exact='wage'
#                     ).values_list('dst_id', flat=True)))
#
#                     if identifier.id in monirs_squad:
#                         self["labels"].append("charity")
#                         self["labels"].append("transfer")
#
#         if "Check for Transaction Count":
#             uses = transactions.count()
#             if uses > 10:
#                 self["labels"].append("m10trx")
#                 self["labels"].append("limit_pwa")
#
#             if uses > 25:
#                 self["labels"].append("m25trx")
#
#                 if "business" in self["labels"]:
#                     self["labels"].append("transfer")
#
#             if uses > 100:
#                 self["labels"].append("m100trx")
#                 self["labels"].append("transfer")
#
#             if uses > 1000:
#                 self["labels"].append("m1000trx")
#
#         self["labels"] = list(set(self["labels"]))
#
#         # Add programs to self profile only if not already assigned
#         assigned_program_keys = Assign.objects.filter(customer=me).values_list('program__key', flat=True)
#         unassigned_programs = Program.objects.exclude(key__in=assigned_program_keys)
#         self["programs"] = [program_api(program) for program in unassigned_programs]
#
#         profiles.append(self)
#
#     if 'Only Want Me' and keys == ['self']:
#         return profiles
#
#     business_stack = me.businesses.A()
#     if 'Check for Business Customers':
#         transactions = iTransaction.f(dst__exact=me, trans_type__in=['product', 'subscription', 'manual'])
#
#         if keys:
#             transactions = transactions.af(src__key__in=keys)
#
#         customers = User.f(id__in=list(set([x.src_id for x in transactions])))
#         for customer in customers:
#             for business in business_stack:
#                 config = business.subscription.config
#
#                 business_orders = business.detect_customer(customer)
#                 if "Check Business Customer" and business_orders:
#                     if "General Data":
#                         transactions = transactions.f(src__exact=customer)
#                         create = min([x.create.timestamp() for x in transactions] + [customer.create.timestamp()])
#                         update = max([x.update.timestamp() for x in transactions] + [customer.update.timestamp()])
#                         resp = {
#                             "create": create,
#                             "update": update,
#                             "key": customer.key,
#                             "business_key": business.key,
#                             "order_details": {},
#                             "group_details": {},
#                             "subscription_details": {}
#                         }
#
#                     if "Order's History Data":
#                         if "Total":
#                             total_orders_count = business_orders.count()
#                             total_orders_amount = business_orders.aggregate(Sum("amount"))['amount__sum'] or 0
#
#                             resp['order_details']['total_orders_count'] = total_orders_count
#                             resp['order_details']['total_orders_amount'] = total_orders_amount
#                             resp['order_details']['average_orders_amount'] = round(
#                                 total_orders_amount / total_orders_count,
#                                 4
#                             )
#
#                         if "Last Month":
#                             last_month_orders = business_orders.f(create__gte=datetime.now() - timedelta(days=30))
#                             last_month_orders_count = last_month_orders.count()
#                             last_month_orders_amount = last_month_orders.aggregate(Sum("amount"))['amount__sum'] or 0
#
#                             resp['order_details']['last_month_orders_count'] = last_month_orders_count
#                             resp['order_details']['last_month_orders_amount'] = last_month_orders_amount
#
#                         if "Current Group Information":
#                             from Business.models import CustomerGroup
#                             groups = CustomerGroup.detect_group(business=business, customer=customer)
#                             if "Customer is Have One or Several Groups" and groups:
#                                 resp['order_details']['group_requirements'] = []
#
#                                 for group in groups:
#                                     title = group.subscription_service.title if group.subscription_service else None
#                                     resp['order_details']['group_requirements'].append(
#                                         GROUP_REQUIREMENTS_DETAILS(group.key, title))
#
#                     if "Customer's Groups Data" and config['features']['customerGroups'] and groups:
#                         resp['group_details'] = {
#                             'current_groups': [],
#                             'chart_trends': []
#                         }
#
#                         if "Current Groups":
#                             for group in groups:
#                                 resp['group_details']['current_groups'].append(group.short_api())
#
#                         if "Group Logs":
#                             groups_logs = customer.CustomerGroupLog.A()
#                             if "Add Group logs to Response" and groups_logs:
#                                 start = groups_logs[0].create
#                                 end = datetime.now()
#                                 sell_count_weeks = find_weeks_v2(start, end, {
#                                     "main": 0,
#                                     "sub": 0
#                                 })
#
#                                 groups_logs = (groups_logs.annotate(
#                                     start_week=Trunc(
#                                         "create",
#                                         kind='week',
#                                         output_field=DateTimeField()
#                                     )).values("start_week").annotate(main=Sum("current_index"))
#                                                ).annotate(sub=Sum("next_index"))
#
#                                 if groups_logs:
#                                     chart_weekly_group_logs = copy.deepcopy(sell_count_weeks)
#                                     for data in list(groups_logs):
#                                         d = data['start_week'].isocalendar()[:2]  # e.g. (2011, 52)
#                                         year_week_id = '{}{:02}'.format(*d)  # e.g. "201152"
#
#                                         # Update the dictionary
#                                         chart_weekly_group_logs[year_week_id] = {
#                                             'main': data['main'],
#                                             'sub': data['main']
#                                         }
#
#                                         resp['group_details']['chart_trends'] = chart_weekly_group_logs
#
#                     if "Customer's Subscriptions Data" and config['features']['subscriptions']:
#                         if "Presence-Absence":
#                             resp['subscription_details']['presence_absence'] = 0
#
#                         from Business.models import Subscription
#                         subscriptions = Subscription.f(
#                             customer__exact=customer,
#                             service__provider__exact=business
#                         ).order_by('create')
#
#                         if "Active Subscriptions":
#                             active_subscriptions = subscriptions.f(expire__gte=datetime.now())
#
#                             if "There is an Active Subscriptions" and active_subscriptions:
#                                 resp['subscription_details']['active_subscriptions'] = []
#                                 for subscription in active_subscriptions:
#                                     resp['subscription_details']['active_subscriptions'].append(
#                                         {
#                                             "subscription_key": subscription.key,
#                                             "remained_days": (subscription.expire - datetime.now()).days,
#                                         }
#                                     )
#
#                         if "Calculate Activity Percentage" and subscriptions:
#                             now = datetime.now()
#                             last_year = now.replace(year=now.year - 1)
#                             total_subscriptions_days = subscriptions.f(create__gte=last_year).aggregate(
#                                 Sum("cost_model__interval"))['cost_model__interval__sum'] or 0
#
#                             try:
#                                 coverage_percentage = round((total_subscriptions_days / 365) * 100, 2)
#                             except IndexError:
#                                 coverage_percentage = 0
#
#                             resp['subscription_details']['last_year_activity_percentage'] = coverage_percentage
#
#                     if "Add Resp to Profiles":
#                         profiles.append({
#                             **customer_api(customer),
#                             **resp
#                         })
#
#         return profiles
#
#
#در این نسخه، ابتدا کلیدهای برنامه‌های اختصاص داده شده به کاربر فعلی از مدل Assign استخراج می‌شود. سپس برنامه‌هایی که هنوز به کاربر اختصاص داده نشده‌اند، از مدل Program استخراج می‌شوند و به پروفایل کاربر اضافه می‌شوند.


import copy
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Sum, DateTimeField
from django.db.models.functions import Trunc

from AppBase.usage import usage
from Business.text import GROUP_REQUIREMENTS_DETAILS
from Platform.models import User, iTransaction, iTGift,Program, Assign, Permission
from toolkit import find_weeks_v2


def customer_api(self):
    response = {
        "key": self.key,
        "total_amount": self.amount,
        "create": self.create.timestamp(),
        "expire": self.expire.timestamp() if self.expire else False,
        "description": self.description,
        "link": self.config['url'] if 'url' in self.config.keys() else None,
        "products": [],
        "services": [],
        "businesses": {},
    }


def self_api(self, more_fields=None):
    if more_fields is None:
        more_fields = []

    fields = ["fullname", "profile"] + more_fields

    response = {
        "username": self.username,
        "taxi": {}
    }
    information = self.information

    for x in fields:
        try:
            response[x] = information[x]
        except KeyError:
            response[x] = None

    return response


def program_api(program):
    return {
        "name": program.name,
        "key": program.key,
        "permissions": [permission.key for permission in program.permissions.all()]
    }


@usage
def load_profiles_v4(request):
    try:
        me = request.DEVICE.user
    except AttributeError:
        return 401
    try:
        keys = request.data['keys']
    except (KeyError, AttributeError, TypeError):
        keys = None

    profiles = []

    if 'My Profile' and (not keys or 'self' in keys):
        virsa = me.assets.g(plan_ilink__exact=settings.VIRSA_PLAN_KEY)
        virdo = me.assets.g(plan_ilink__exact=settings.VIRDO_PLAN_KEY)
        virdo_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRDO_PLAN_KEY)
        virsa_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRSA_PLAN_KEY)
        virdaar_old = me.assets.g(plan_ilink__exact=settings.OLD_VIRDAR_PLAN_KEY)

        gifts = iTGift.f(expire__gt=datetime.now())

        self = {
            **self_api(me, more_fields=['mobile', 'email', 'shaparak_payout', 'shaparak_cash']),
            **{
                "virsa": virsa.count if virsa else 0,
                "virdo": virdo.count if virdo else 0,
                "virdo_old": virdo_old.count if virdo_old else 0,
                "virsa_old": virsa_old.count if virsa_old else 0,
                "virdaar_old": virdaar_old.count if virdaar_old else 0,

                "magic_charge": float(me.magic_charge_rate),
                "blocked_cash": sum([x.amount for x in iTransaction.f(trans_type__exact='blocked', src__exact=me)]),
                "key": "self",
                "identifier": me.identifier,
                "create": me.create.timestamp(),
                "update": me.update.timestamp(),
                "labels": [],
                "beta": {
                    "join": me.meta('beta-program-enrollment'),
                    "expire": me.meta('beta-program-expired')
                },
                "ux": {}
            }
        }

        transactions = iTransaction.f_or(src__exact=me, dst__exact=me)

        if "Check for Limited Bill User" and transactions.count() >= 15:
            self["labels"].append("charity")
            self["labels"].append("pay_bill")
            self["labels"].append("pay_consumption")
            self["labels"].append("transfer_money")

        if "Check for Blocked User":
            if me.status == 'blocked':
                self["labels"].append("blocked")

        if "Check for Limited User":
            if me.status == 'limited':
                self["labels"].append("limited")

        if "Check for Venture Customer":
            is_venture_customer = transactions.f(trans_type__in=['unit', 'gift_unit', 'unit_transaction']).count() > 0
            if is_venture_customer:
                self["labels"].append("venture")

        if "Check for Business Customer":
            business_stack = me.businesses.A()
            business_uses = business_stack.count()

            if business_uses > 0:
                self["labels"].append("business")

            if business_uses > 1:
                self["labels"].append("multi_business")

            if business_uses == 1:
                self["ux"]["business"] = business_stack[0].brand

        if "Monirs Squad":
            if 'charity' not in self["labels"] or 'transfer' not in self["labels"]:
                identifier = User.k(me.meta('identifier'))
                if identifier:
                    monirs_squad = list(set(iTransaction.f(
                        src_id__exact=28,
                        trans_type__exact='wage'
                    ).values_list('dst_id', flat=True)))

                    if identifier.id in monirs_squad:
                        self["labels"].append("charity")
                        self["labels"].append("transfer")

        if "Check for Transaction Count":
            uses = transactions.count()
            if uses > 10:
                self["labels"].append("m10trx")
                self["labels"].append("limit_pwa")

            if uses > 25:
                self["labels"].append("m25trx")

                if "business" in self["labels"]:
                    self["labels"].append("transfer")

            if uses > 100:
                self["labels"].append("m100trx")
                self["labels"].append("transfer")

            if uses > 1000:
                self["labels"].append("m1000trx")

        self["labels"] = list(set(self["labels"]))

        # Add programs to self profile
        programs = Assign.objects.filter(customer=me).select_related('program')
        self["programs"] = [program_api(assign.program) for assign in programs]

        profiles.append(self)

    if 'Only Want Me' and keys == ['self']:
        return profiles

    business_stack = me.businesses.A()
    if 'Check for Business Customers':
        transactions = iTransaction.f(dst__exact=me, trans_type__in=['product', 'subscription', 'manual'])

        if keys:
            transactions = transactions.af(src__key__in=keys)

        customers = User.f(id__in=list(set([x.src_id for x in transactions])))
        for customer in customers:
            for business in business_stack:
                config = business.subscription.config

                business_orders = business.detect_customer(customer)
                if "Check Business Customer" and business_orders:
                    if "General Data":
                        transactions = transactions.f(src__exact=customer)
                        create = min([x.create.timestamp() for x in transactions] + [customer.create.timestamp()])
                        update = max([x.update.timestamp() for x in transactions] + [customer.update.timestamp()])
                        resp = {
                            "create": create,
                            "update": update,
                            "key": customer.key,
                            "business_key": business.key,
                            "order_details": {},
                            "group_details": {},
                            "subscription_details": {}
                        }

                    if "Order's History Data":
                        if "Total":
                            total_orders_count = business_orders.count()
                            total_orders_amount = business_orders.aggregate(Sum("amount"))['amount__sum'] or 0

                            resp['order_details']['total_orders_count'] = total_orders_count
                            resp['order_details']['total_orders_amount'] = total_orders_amount
                            resp['order_details']['average_orders_amount'] = round(
                                total_orders_amount / total_orders_count,
                                4
                            )

                        if "Last Month":
                            last_month_orders = business_orders.f(create__gte=datetime.now() - timedelta(days=30))
                            last_month_orders_count = last_month_orders.count()
                            last_month_orders_amount = last_month_orders.aggregate(Sum("amount"))['amount__sum'] or 0

                            resp['order_details']['last_month_orders_count'] = last_month_orders_count
                            resp['order_details']['last_month_orders_amount'] = last_month_orders_amount

                        if "Current Group Information":
                            from Business.models import CustomerGroup
                            groups = CustomerGroup.detect_group(business=business, customer=customer)
                            if "Customer is Have One or Several Groups" and groups:
                                resp['order_details']['group_requirements'] = []

                                for group in groups:
                                    title = group.subscription_service.title if group.subscription_service else None
                                    resp['order_details']['group_requirements'].append(
                                        GROUP_REQUIREMENTS_DETAILS(group.key, title))

                    if "Customer's Groups Data" and config['features']['customerGroups'] and groups:
                        resp['group_details'] = {
                            'current_groups': [],
                            'chart_trends': []
                        }

                        if "Current Groups":
                            for group in groups:
                                resp['group_details']['current_groups'].append(group.short_api())

                        if "Group Logs":
                            groups_logs = customer.CustomerGroupLog.A()
                            if "Add Group logs to Response" and groups_logs:
                                start = groups_logs[0].create
                                end = datetime.now()
                                sell_count_weeks = find_weeks_v2(start, end, {
                                    "main": 0,
                                    "sub": 0
                                })

                                groups_logs = (groups_logs.annotate(
                                    start_week=Trunc(
                                        "create",
                                        kind='week',
                                        output_field=DateTimeField()
                                    )).values("start_week").annotate(main=Sum("current_index"))
                                               ).annotate(sub=Sum("next_index"))

                                if groups_logs:
                                    chart_weekly_group_logs = copy.deepcopy(sell_count_weeks)
                                    for data in list(groups_logs):
                                        d = data['start_week'].isocalendar()[:2]  # e.g. (2011, 52)
                                        year_week_id = '{}{:02}'.format(*d)  # e.g. "201152"

                                        # Update the dictionary
                                        chart_weekly_group_logs[year_week_id] = {
                                            'main': data['main'],
                                            'sub': data['main']
                                        }

                                        resp['group_details']['chart_trends'] = chart_weekly_group_logs

                    if "Customer's Subscriptions Data" and config['features']['subscriptions']:
                        if "Presence-Absence":
                            resp['subscription_details']['presence_absence'] = 0

                        from Business.models import Subscription
                        subscriptions = Subscription.f(
                            customer__exact=customer,
                            service__provider__exact=business
                        ).order_by('create')

                        if "Active Subscriptions":
                            active_subscriptions = subscriptions.f(expire__gte=datetime.now())

                            if "There is an Active Subscriptions" and active_subscriptions:
                                resp['subscription_details']['active_subscriptions'] = []
                                for subscription in active_subscriptions:
                                    resp['subscription_details']['active_subscriptions'].append(
                                        {
                                            "subscription_key": subscription.key,
                                            "remained_days": (subscription.expire - datetime.now()).days,
                                        }
                                    )

                        if "Calculate Activity Percentage" and subscriptions:
                            now = datetime.now()
                            last_year = now.replace(year=now.year - 1)
                            total_subscriptions_days = subscriptions.f(create__gte=last_year).aggregate(
                                Sum("cost_model__interval"))['cost_model__interval__sum'] or 0

                            try:
                                coverage_percentage = round((total_subscriptions_days / 365) * 100, 2)
                            except IndexError:
                                coverage_percentage = 0

                            resp['subscription_details']['last_year_activity_percentage'] = coverage_percentage

                    if "Add Resp to Profiles":
                        profiles.append({
                            **customer_api(customer),
                            **resp
                        })

        return profiles


# در این کد، تابع program_api اطلاعات برنامه‌ها و مجوزهای مربوطه را استخراج می‌کند. سپس این تابع در load_profiles_v4 فراخوانی می‌شود تا برنامه‌ها به پروفایل کاربر اضافه شوند.