from datetime import datetime

from django.utils import timezone

from AppBase.usage import usage
from Business.models import SubscriptionServiceCostModel, iTSubscription, Subscription, SubscriptionService
from Business.models import Taxi
from Platform.external_services.raygan_sms import send_sms
from Platform.models import Cache, iTransaction, User, Device
from toolkit import load_request_payment_flags


def api(self, for_id=False):
    response = {
        "key": self.key,
        "car_type": self.car_type,
        "taxi_code": self.taxi_code,

        "taxi_license_plate": self.taxi_license_plate,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed
    }
    if not for_id:
        response["taxi_driver"] = self.taxi_driver.api()

    return response


@usage
def add_taxi_v1abcd12(req, d, device):
    try:
        mobile = d["mobile"] if 'mobile' in d.keys() else False
        customer_name = d["customer_name"] if 'customer_name' in d.keys() else False
        plaque_city = d['plaque_city']
        plaque_d2 = d['plaque_d2']
        plaque_alphabet = d['plaque_alphabet']
        plaque_d3 = d['plaque_d3']
        taxi_code = d['taxi_code']
        city_ilink = d['city']
        car_type = d['car_type']
        taxi_license_plate = plaque_d2 + "," + plaque_alphabet + "," + plaque_d3 + "," + plaque_city
        by_virdaar, by_card = load_request_payment_flags(d)
    except:
        return 400

    try:
        customer = device.user
        mobile = customer.mobile
        if len(customer.driver.all()) >= 1:
            return 409
    except:
        customer = User.find_user(mobile)
        if customer:
            return 405

        customer = User(
            username=mobile,
        )
        customer.save()
        device = Device(user=customer, agent=req.META["HTTP_USER_AGENT"])
        device.save()
        customer.meta_update('fullname', customer_name)

        header = '{} عزیز ورودتون رو به خانواده ویردار تبریک میگیم.\n'.format(customer_name)
        body = 'لطفا برای ادامه روی یکی از لینک های زیر کلیک کنین:\n'
        app_link = 'نسخه اندروید:\n https://drive.google.com/file/d/1HdTMCWCnWOX5npGG9MLaugyoaY7PznYn/view'
        site_link = 'نسخه ios:\n https://virdaar.ir'
        footer = 'ویردار، فناوری برای زندگی'
        if not send_sms(mobile, header + body + app_link + '\n' + site_link + '\n' + footer):
            return 502

    service = SubscriptionService.k('rc')
    cost_model = SubscriptionServiceCostModel.k('Z')
    commission = 0
    transaction_amount = cost_model.cost + commission

    # transaction_amount, gift_balance = Gift.gift_calculator(transaction_amount, 'virdar', customer,
    #                                                         part='subscription')
    if by_card == 1 and transaction_amount:
        payment_token, payment_url = Cache.pay_by_card(transaction_amount, d, device)
        return 402, {"link": payment_url, "token": payment_token}

    transaction = iTransaction(
        amount=cost_model.cost,
        src=customer,
        dst_id=1,
        trans_type="subscription",
        trashed=True
    )
    transaction.save()

    expire = timezone.now() + timezone.timedelta(days=cost_model.interval)
    subscription = Subscription.g(cost_model__exact=cost_model, service__exact=service, customer__exact=customer)

    if not subscription:
        subscription = Subscription(
            service=service,
            expire=expire,
            customer=customer,
            cost_model=cost_model,
        )
    else:
        if subscription.expire <= datetime.now():
            subscription.expire = expire
        else:
            subscription.expire += timezone.timedelta(days=cost_model.interval)

    subscription.save()

    # TODO :Save Expire Notification
    subscription_transaction = iTSubscription(transaction=transaction, subscription=subscription)
    subscription_transaction.save()

    try:
        taxi = Taxi(
            taxi_license_plate=taxi_license_plate,
            city_ilink=city_ilink,
            car_type=car_type,
            taxi_code=taxi_code,
            taxi_driver=customer,
            subscription=subscription
        )
        taxi.save()
    except:
        return 502

    transaction.trashed = False
    transaction.save()
    customer.update_balance()

    return 200, taxi.api()
