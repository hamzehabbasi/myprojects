import json
import os
import zipfile
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from django.core.files.storage import default_storage
from django.core import serializers

from PaymentXM.models import *
from PlatformXM.models import *
from Platform.models import *
from Business.models import *
from Venture.models import *
from Payment.models import *
from Charity.models import *


def pick_one(queryset_item):
    return json.loads(serializers.serialize('json', [queryset_item]))[0]


def pick_all(queryset):
    return json.loads(serializers.serialize('json', queryset))


def prepare_customer_basic_data(customer):
    return {
        "user": pick_one(customer),
        "metadata": pick_all(customer.metas.all()),
        "devices": pick_all(customer.devices.all()),
        "option": pick_one(customer.options)
    }


def prepare_customer_transaction_data(customer):
    internal_transactions = iTransaction.f_or(src__exact=customer, dst__exact=customer)
    internal_transactions_ids = [x.keys for x in internal_transactions]

    external_transactions = Transaction.f(user__exact=customer)
    return {
        "internal": pick_all(internal_transactions),
        "external": pick_all(external_transactions),
        "iTTaxi": pick_all(iTTaxi.f(transaction__key__in=internal_transactions_ids)),
        "iTUnit": pick_all(iTUnit.f(transaction__key__in=internal_transactions_ids)),
        "iTTransfer": pick_all(iTTransfer.f(transaction__key__in=internal_transactions_ids)),
        "iTBill": pick_all(iTBill.f(transaction__key__in=internal_transactions_ids)),
        "iTCharityPayment": pick_all(iTCharityPayment.f(transaction__key__in=internal_transactions_ids)),
        "iTCharge": pick_all(iTCharge.f(transaction__key__in=internal_transactions_ids)),
        "iTOff": pick_all(iTOff.f(transaction__key__in=internal_transactions_ids)),
        "iTGift": pick_all(iTGift.f(transaction__key__in=internal_transactions_ids)),
        "iTBlock": pick_all(iTBlock.f(transaction__key__in=internal_transactions_ids)),
        "iTSubscription": pick_all(iTSubscription.f(transaction__key__in=internal_transactions_ids)),
        "iTProduct": pick_all(iTProduct.f(transaction__key__in=internal_transactions_ids)),
        "iTWage": pick_all(iTWage.f(transaction_ilink__in=internal_transactions_ids)),
        "iTManual": pick_all(iTManual.f(transaction__key__in=internal_transactions_ids)),
        "iTSubscriptionCancel": pick_all(iTSubscriptionCancel.f(transaction__key__in=internal_transactions_ids))
    }


def prepare_business_data(business):
    order_customers = User.f(id__in=[o.customer.id for o in business.business_orders.all()])
    subscription_customers = User.f(id__in=[o.customer.id for o in Subscription.f(service__provider__exact=business)])
    business_customers = subscription_customers | order_customers
    return {
        "business": pick_one(business),
        "owner": prepare_customer_basic_data(business.customer),
        "transactions": prepare_customer_transaction_data(business.customer),
        "products": pick_all(business.products.all()),
        "orders": pick_all(business.business_orders.all()),
        "customers": [prepare_customer_basic_data(each) for each in business_customers],
    }


class Command(BaseCommand):
    help = 'Exports VIRDAR Data'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument(
            '--system',
            action='store_true',
            help='Export the system data',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--variant',
            type=str,
            choices=['cafe-perisce', 'cafe-blaze'],
            help='Export data for the specified variant',
        )

        parser.add_argument(
            '--customer',
            type=str,
            help='Export data for the specified customer',
        )

        parser.add_argument(
            '--business',
            type=str,
            help='Export data for the specified business',
        )

    def handle(self, *args, **options):
        if options['system']:
            self.export_system()
        elif options['variant']:
            self.export_variant(options['variant'])
        elif options['customer']:
            self.export_customer(options['customer'])
        elif options['business']:
            self.export_business(options['business'])
        else:
            raise CommandError('No valid export type specified')

    def export_system(self):
        self.stdout.write('Exporting system data...')

        response = {
            "terms": pick_all(Term.A()),
            "cities": pick_all(City.A()),
            "provinces": pick_all(Province.A()),
            "contents": pick_all(Content.A()),
            "faqs": pick_all(Faq.A()),
            "metadata": pick_all(Metadata.f(customer__exact=None)),
            "accounts": [prepare_customer_basic_data(each) for each in User.f(key__startswith='__')],
        }

        uri = f"export-system-{str(datetime.now())}.json"
        with open(uri, 'w+') as f:
            json.dump(response, f)

        self.create_zip_file(uri)
        self.stdout.write(self.style.SUCCESS(f"Export Saved into {uri}.zip"))

    def export_variant(self, variant):
        self.stdout.write(self.style.SUCCESS(f'Exporting variant data for {variant}...'))
        # Your export logic here

    def export_customer(self, customer_id):
        customer = self.find_customer(customer_id)
        if not customer:
            self.stdout.write(self.style.NOTICE(f"Customer {customer_id} does not exist"))
            return

        self.stdout.write(self.style.SUCCESS(f'Exporting customer data for {customer.username} ({customer.id})...'))

        usage_ids = [x.id for device in customer.devices.all() for x in Usage.f(request__headers__HTTP_API_KEY=device.ui_token)]
        usages = Usage.f(id__in=usage_ids)

        response = {
            "type": "export-customer",
            "id": customer_id,
            **prepare_customer_basic_data(customer),
            "transactions": prepare_customer_transaction_data(customer),
            "usages": pick_all(usages),
            "devices": pick_all(customer.devices.all()),
            "option": pick_one(customer.options)
        }

        uri = f"export-customer-{customer.key}-{str(customer.id)}-{customer.username}-{str(datetime.now())}.json"
        with open(uri, 'w+') as f:
            json.dump(response, f)

        self.create_zip_file(uri)
        self.stdout.write(self.style.SUCCESS(f"Export Saved into {uri}.zip"))

    def export_business(self, business_id):
        if not business_id.startswith("@"):
            self.stdout.write(self.style.ERROR("business id should be like @nutella"))
            return

        business = Business.k(business_id[1:])
        if not business:
            self.stdout.write(self.style.NOTICE(f"Business {business_id} does not exist"))
            return

        self.stdout.write(f'Exporting business data for {business_id}...')

        response = {
            "type": "export-business",
            "id": business_id,
            **prepare_business_data(business)
        }

        uri = f"export-business-{business_id}-{str(datetime.now())}.json"
        with open(uri, 'w+') as f:
            json.dump(response, f)

        self.create_zip_file(uri)
        self.stdout.write(self.style.SUCCESS(f"Export Saved into {uri}.zip"))

    def create_zip_file(self, json_file_path):
        zip_file_path = f"{json_file_path}.zip"
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_file_path, os.path.basename(json_file_path))
        os.remove(json_file_path)

    def find_customer(self, customer_id):
        customer = User.find_user(customer_id) or User.i(customer_id) or User.k(customer_id)
        return customer
