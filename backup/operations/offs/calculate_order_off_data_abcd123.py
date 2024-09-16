from datetime import datetime

from Business.models import iTSubscription, Subscription


def calculate_order_off_data_abcd1234(each, business, customer, available_offs, off_code):
    offs = []
    config = business.subscription.config['features']

    for off in available_offs:
        if "Initialize Off Data":
            off_data = {
                "key": off.key,
                "amount": 0,
                "count": each['count'],
                "affect_type": off.affect_type,
                "title": off.title,
                "code": off_code
            }

        if "Verify Off Code" and config['offDiscountCode']:
            if off.code and off.code != off_code:
                continue

        if "Check Expire Date" and config['offDate']:
            if off.expire_date and off.expire_date <= datetime.now():
                continue

        # if "Check For Customer Group" and config['offCustomerGroup']: #@todo activate
        # group_member = off.customers_groups.A()
        # if group_member and customer not in group_member:
        #     continue

        # if "Check For Loyal Customer" and customer and config['offLoyalCustomers']:
        #     if off.for_loyal_customers:
        #         if role != 'buyer':
        #             continue
        #
        #         if not business.is_loyal_customer(customer):
        #             continue # @TODO

        if "Check For Continuous Subscription Service" and customer and config['offContinuousSubscribes']:
            if off.for_continuous_subscription_service and "cost_model_key" in each.keys():
                if "Has An Subscription":
                    subscription = Subscription.g(service__key__exact=each['key'], customer__exact=customer)
                    if not subscription:
                        continue

                    renew_transactions = iTSubscription.f(
                        subscription__service__key__exact=each['key'],
                        transaction__src__exact=customer,
                    ).order_by('create')

                    if renew_transactions.count() == 0:
                        continue

                if "How Many Days":
                    off_days = 0
                    previous_expire_time = renew_transactions[0].expire
                    for payment in renew_transactions:
                        if off.for_continuous_subscription and payment.create - previous_expire_time > 0:
                            off_days = 0

                        off_days += (payment.expire - payment.create).days

                power = off_days / off.for_continuous_subscription_base_duration
                off_data["amount"] = each['base_price'] * pow(1 - off.off_percent_amount, power)

        if "Check For Upto Certain Sell Count" and config['offUptoCertainCount']:
            if off.upto_certain_sell_count:
                available = off.upto_certain_sell_count - off.data['upto_certain_sell_count_consumed']
                off_data['count'] = min(available, off_data['count'])

        if "Off Fixed Amount or Off Fixed Percent":
            if off.off_type == "off_fixed_amount":
                off_data['amount'] = off.off_amount * off_data['count']
            else:
                off_data['amount'] = round(each['base_price'] * off_data['count'] * (off.off_amount / 100), 4)

        if "Check For Off Budget" and config['offBudget']:
            if off.off_budget:
                available = max(0, off.off_budget - off.data['off_budget_consumed'])
                available = float(round((available * off.release_percent) / 100, 4))

                off_data['amount'] = min(off_data['amount'], available)

        if "Check For Upto Certain Sell Amount" and config['offUptoCertainAmount']:
            if off.upto_certain_sell_amount:
                available = max(0, off.upto_certain_sell_amount - off.data['upto_certain_sell_amount_consumed'])
                off_data['amount'] = min(off_data['amount'], available)

        if "Check For More Than Amount" and config['offMoreThanAmount']:
            if off.for_more_than_amount and each['base_price'] < off.for_more_than_amount:
                continue
            if off.for_more_than_amount:
                if round(each['base_price'] * off_data['count'], 4) < off.for_more_than_amount:
                    continue

        offs.append(off_data)
    if len(offs) > 0:
        each['off_data'] = sorted(offs, key=lambda x: x["amount"], reverse=True)[0]
        each['off'] = each['off_data']['amount']

    return each
