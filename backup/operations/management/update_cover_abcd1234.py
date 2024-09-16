from datetime import timedelta, datetime

from AppBase.usage import usage
from Business.text import *
from toolkit import image_base64_upload


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
def update_cover_abcd1234(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user
            business = customer.businesses.k(d['business_key'])
            _ = business.key

            image = d["image"]
        except (ValueError, KeyError, AttributeError):
            return 400

        if 'Upload New Image' and image and not image.startswith("https"):
            image_name, image_data = image_base64_upload(image)
            business.cover.save(image_name, image_data)

    if 'Save and Update Flags':
        customer.save_synchronize_flag('businesses', business.pk)

    return business.administrator_api()
