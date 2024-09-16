from datetime import timedelta, datetime

import jdatetime

from AppBase.usage import usage
from Business.models import Business
from Business.models import SubscriptionServiceCostModel, iTSubscription, Subscription, SubscriptionService
from Business.text import *
from Platform.models import User, iTransaction, Prompt, ID
from PlatformXM.models import City
from toolkit import load_request_payment_flags


def administrator_api(self):
    information = self.business_information
    telephone_key = 'business_' + self.key + '_link_telephone'
    address_key = 'business_' + self.key + '_link_address'
    if "Check Config":
        config = self.subscription.config
        config['icons']['vitrine'] = {}
        config['themes']['web']['vitrine'] = {}
        config['themes']['android']['vitrine'] = {}
        config['i18n']['fa']['vitrine'] = {}

    if "Detect Evaluated":
        next_thirty_days = datetime.now() + timedelta(days=30)
        validate_license_date = self.license_date >= next_thirty_days if self.license_date else False
        validate_limitations = self.check_limits()
        license_number_validate = self.license_number if self.license_number else None
        validate_evaluated = validate_license_date and license_number_validate and validate_limitations

    return {
        "key": self.key,
        "has_store": True if self.subscription.service.key in ['Bs', 'Ai', 'Bb', 'rs', 'Rs'] else None,
        "title": self.title,
        "brand": self.brand,
        "description": self.description,
        "license_number": self.license_number,
        "license_expire": self.license_date.timestamp() if self.license_date else None,
        "telephone": information[telephone_key] if telephone_key in information.keys() else None,
        "address": information[address_key] if address_key in information.keys() else None,
        "city": {
            "key": self.city_ilink,
            "value": self.city.name if self.city else None
        },
        "logo": (settings.VIRDAAR_ENDPOINT_URL + self.logo.name) if self.logo else False,
        "cover": (settings.VIRDAAR_ENDPOINT_URL + self.cover.name) if self.cover else False,
        "create": self.create.timestamp(),
        "update": self.update.timestamp(),
        "active": not self.trashed,
        "turn_rating": self.turn_ratings,
        "licence_number": self.license_number,
        "subscription_key": self.subscription.key,
        "service_key": self.subscription.service.key,
        "config": config,
        "evaluated": validate_evaluated
    }


@usage
def add_business_abcd1234(req, d, device):
    if 'Validate Request and Initialize':
        try:
            title = d["title"]
            address = d["address"]
            brand = d["brand"].lower()
            telephone = d["telephone"] if 'telephone' in d.keys() else False

            city_ilink = d["city"]
            _ = City.k(city_ilink)

            cost_model = SubscriptionServiceCostModel.k(d['cost_model_key'])
            service = SubscriptionService.k(d['service_key'])
            service_by_cost_model = cost_model.service

            if service_by_cost_model != service:
                raise ValueError

            transaction_amount = cost_model.cost

            license_number = d['license_number']
            license_date = d['license_expire']
            [year, month, day] = license_date.split("/")
            try:
                license_expire = jdatetime.datetime(int(year), int(month), int(day)).togregorian()
            except ValueError:
                if month == 12 and day == 30:
                    license_expire = jdatetime.datetime(int(year), int(month), int(29)).togregorian()

            mobile = d["mobile"] if 'mobile' in d.keys() else False
            customer_name = d["customer_name"] if 'customer_name' in d.keys() else False

            validate_customer_name = type(customer_name) is str and len(customer_name) >= 3
            validate_mobile = type(mobile) is str and len(mobile) == 11 and mobile.starswith("09")
            validate_customer = device or (validate_customer_name and validate_mobile)

            validate_business_data = 3 <= len(title) <= 50 and len(address) > 7 and 5 <= len(brand) <= 50
            validated_expire = license_expire.replace(hour=23, minute=59, second=59)
            validate_licence = len(license_number) == 10 and validated_expire >= datetime.now() + timedelta(days=10)

            validate = validate_business_data and validate_licence and validate_customer

            if not validate:
                raise ValueError

            by_virdaar, by_card = load_request_payment_flags(d)
            virdaar_amount = 0
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Verify Business Brand':
        id_validate = ID.validate(brand)
        if not id_validate:
            return 409

    if 'Verify Customer Account or Make an account for him/her':
        try:
            customer = device.user
            mobile = customer.mobile
        except AttributeError:
            customer = User.find_user(mobile)
            if customer:
                return 405

            parameters, template_id = REGISTER_BUSINESS_WELCOME_LEAD(customer_name, template=True)
            customer, device = User.lead(
                mobile,
                customer_name,
                req,
                parameters,
                template_id
            )

    if 'Direct Buy by VIRDAR units':
        if by_virdaar == 1:
            virdaar_amount = transaction_amount
            transaction_amount = 0

    if 'Check for Balance':
        if "Calculate Tax And Add Amount To Reqeust":
            tax = ((transaction_amount + virdaar_amount) * 9) / 100
            transaction_amount = transaction_amount + virdaar_amount + tax
            d['amount'] = transaction_amount

        balance_status, balance_response, virdaar_checkout, off_data = customer.check_balance(
            virdaar=virdaar_amount,
            cash=transaction_amount,
            service_id=service.key,
            by_card={"request": d, "state": by_card, "device": device}
        )

        if balance_status == 402:
            return 402, balance_response

        if balance_status != 200:
            return balance_status

    if 'Prepare Transaction and Subscription':
        transaction = iTransaction(
            amount=transaction_amount,
            src=customer,
            dst_id=1,
            trans_type="subscription",
            trashed=True
        )
        transaction.save()

        subscription = Subscription(
            service=service,
            expire=datetime.now() + timedelta(days=cost_model.interval),
            customer=customer,
            cost_model=cost_model,
            trashed=True
        )
        subscription.save()

    if 'Register Business':
        business = Business(
            title=title,
            customer=customer,
            brand=brand,
            city_ilink=city_ilink,
            license_number=license_number,
            license_date=license_expire,
            subscription_ilink=subscription.key,
            key=brand,
            trashed=True
        )
        business.save()

        business.meta_update("link_address", address)
        if telephone:
            business.meta_update("link_telephone", telephone)

    if 'Create ID':
        business_id = ID(
            type='business',
            value=brand
        )
        business_id.save()

    if 'Create iTSubscription':
        it_subscription = iTSubscription(
            transaction=transaction,
            subscription=subscription,
            trashed=True
        )
        it_subscription.save()

    if 'Active Transaction, Subscription and Business':
        transaction.trashed = False
        transaction.affect_off(off_data)
        transaction.save()

        it_subscription.trashed = False
        it_subscription.save()

        subscription_title = subscription_title_generator(subscription, business)
        subscription.title = subscription_title
        subscription.trashed = False
        subscription.save()

        business.trashed = False
        business.save()

        customer.update_balance()
        customer.update_assets()

    # if "Create CashBack Off":
    #     business.business_pagosha(subscription)

    if 'Send a prompt':
        message = REGISTER_BUSINESS_CALL_TO_START(service)
        if message:
            Prompt.generate(user=customer, data={'message': message}, prompt_type="call_to_action")

    return business.administrator_api()
