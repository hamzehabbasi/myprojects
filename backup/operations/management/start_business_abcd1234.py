from datetime import timedelta, datetime

from AppBase.usage import usage
from Business.models import Business
from Business.models import Subscription, BusinessProductLabel, VitrineCategory
from Business.text import *
from Platform.external_services.monid_service import check_id, reserve_id
from Platform.models import Prompt, ID


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
def start_business_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            title = d["title"]
            brand = d["brand"].lower()
            demo_key = d["demo_key"]

            demo = Business.k(demo_key)
            if not demo:
                raise ValueError

            cost_model = demo.subscription.cost_model
            service = cost_model.service

        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Verify Business Brand':
        id_validate = ID.validate(brand)
        if not id_validate:
            return 409
        business = Business.g(brand__exact=brand)
        if business:
            return 409

        if "Check Monid For Validate ID":
            status, response = check_id(brand)
            if status == 409:
                return status

    if 'Verify Customer':
        customer = device.user

    if 'Prepare Transaction and Subscription':
        subscription = Subscription(
            service=service,
            expire=datetime.now() + timedelta(days=cost_model.interval),
            customer=customer,
            cost_model=cost_model
        )
        subscription.save()

    if 'Register Business':
        business = Business(
            title=title,
            customer=customer,
            brand=brand,
            subscription_ilink=subscription.key,
            key=brand
        )
        if customer.city:
            business.city_ilink = customer.city.key if customer.city else None

        business.save()

        Business.business_copier(business=business, demo_key=demo_key)

    if 'Create ID':
        business_id = ID(
            type='business',
            value=brand
        )
        business_id.save()

        if "Reserve ID":
            status, response = reserve_id(brand)
            if status == 409:
                return status

    if 'Create Labels':
        config = subscription.config

        labels = config['labels'] if 'labels' in config.keys() else {}
        items = labels['items'] if labels and 'items' in labels.keys() else []
        for item in items:
            product_label = BusinessProductLabel.g(
                business=business,
                name=item['name']
            )

            if "Available Label" and product_label:
                continue

            product_label = BusinessProductLabel(
                business=business,
                color=item['color'],
                name=item['name']
            )
            product_label.save()

    if 'Create Categorize':
        categorizes = config['categorize'] if 'categorize' in config.keys() else None
        if categorizes:
            for category in categorizes:
                old_category = VitrineCategory.g(
                    business=business,
                    name=category['name']
                )

                if "Available Category" and old_category:
                    continue

                new_category = VitrineCategory(
                    name=category['name'],
                    business=business
                )
                new_category.save()

    if 'Active Transaction, Subscription and Business':
        subscription_title = subscription_title_generator(subscription, business)
        subscription.title = subscription_title
        subscription.trashed = False
        subscription.save()

        business.trashed = False
        business.save()

        customer.update_balance()
        customer.update_assets()

    if 'Send a prompt':
        message = REGISTER_BUSINESS_CALL_TO_START(service)
        if message:
            Prompt.generate(user=customer, data={'message': message}, prompt_type="call_to_action")

    return business.administrator_api()
