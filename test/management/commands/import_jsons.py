# import json
# import os
# import shutil
#
# import boto3
# from django.core.management.base import BaseCommand, CommandError
# from django.apps import apps
# from django.conf import settings
# from django.core.files.storage import default_storage
# from django.db import models
#
#
# class Command(BaseCommand):
#     help = 'Import data from JSON into a specific model and copy FileFields/ImageFields with a new name'
#
#     def add_arguments(self, parser):
#         parser.add_argument('app_label', type=str, help='The app label of the model')
#         parser.add_argument('model_name', type=str, help='The model name')
#         parser.add_argument('json_file', type=str, help='The path to the JSON file to import')
#
#     def handle(self, *args, **options):
#         app_label = options['app_label']
#         model_name = options['model_name']
#         json_file = options['json_file']
#
#         try:
#             model = apps.get_model(app_label, model_name)
#         except LookupError:
#             raise CommandError(f'Model "{app_label}.{model_name}" not found.')
#
#         try:
#             with open(json_file, 'r') as file:
#                 data = json.load(file)['contents']
#         except FileNotFoundError:
#             raise CommandError(f'File "{json_file}" not found.')
#         except json.JSONDecodeError:
#             raise CommandError(f'Error decoding JSON from file "{json_file}".')
#         for item in data:
#             pk = item.get('pk')
#             fields = item.get('fields')
#
#             if pk is None or fields is None:
#                 self.stdout.write(self.style.WARNING(f'Skipping invalid item: {item}'))
#                 continue
#
#             for field_name, field_value in fields.items():
#                 field = model._meta.get_field(field_name)
#                 if isinstance(field, (models.FileField, models.ImageField)):
#                     new_file_path = self.copy_file_with_new_name(field_value)
#                     fields[field_name] = new_file_path
#
#             try:
#                 instance, created = model.objects.update_or_create(pk=pk, defaults=fields)
#                 if created:
#                     self.stdout.write(self.style.SUCCESS(f'Created instance with PK {pk}'))
#                 else:
#                     self.stdout.write(self.style.SUCCESS(f'Updated instance with PK {pk}'))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Error processing item with PK {pk}: {e}'))
#
#         # except FileNotFoundError:
#         #     raise CommandError(f'File "{json_file}" not found.')
#
#     def copy_file_with_new_name(self, file_path):
#         if not file_path:
#             return file_path
#
#         # Define the new file name
#         base_name = os.path.basename(file_path)
#         name, ext = os.path.splitext(base_name)
#         new_name = f"{name}_imported{ext}"
#         new_path = os.path.join(os.path.dirname(file_path), new_name)
#
#         # Check if default storage is S3
#         if default_storage.__class__.__name__ == 'S3Boto3Storage':
#             s3_client = boto3.client('s3')
#             bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#
#             copy_source = {
#                 'Bucket': bucket_name,
#                 'Key': file_path
#             }
#
#             try:
#                 s3_client.copy(copy_source, bucket_name, new_path)
#                 self.stdout.write(self.style.SUCCESS(f'Copied file to {new_path}'))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Error copying file: {e}'))
#
#         else:
#             # Local storage case
#             src = os.path.join(settings.MEDIA_ROOT, file_path)
#             dst = os.path.join(settings.MEDIA_ROOT, new_path)
#             shutil.copy(src, dst)
#
#         return new_path
#
# # کد اجرای کد بالا در ترمینال
# # python manage.py import_jsons PlatformXM Content export-system.json


import json
import os
import shutil
import zipfile

import boto3
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models


class Command(BaseCommand):
    help = 'Import data from JSON in a ZIP file into a specific model and copy FileFields/ImageFields with a new name'

    def add_arguments(self, parser):
        parser.add_argument('app_label', type=str, help='The app label of the model')
        parser.add_argument('model_name', type=str, help='The model name')
        parser.add_argument('zip_file', type=str, help='The path to the ZIP file containing the JSON file to import')

    def handle(self, *args, **options):
        app_label = options['app_label']
        model_name = options['model_name']
        zip_file = options['zip_file']

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f'Model "{app_label}.{model_name}" not found.')

        json_file = self.extract_json_from_zip(zip_file)
        if not json_file:
            raise CommandError(f'No valid JSON file found in the ZIP archive "{zip_file}".')

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)['contents']
        except FileNotFoundError:
            raise CommandError(f'File "{json_file}" not found.')
        except json.JSONDecodeError:
            raise CommandError(f'Error decoding JSON from file "{json_file}".')

        for item in data:
            pk = item.get('pk')
            fields = item.get('fields')

            if pk is None or fields is None:
                self.stdout.write(self.style.WARNING(f'Skipping invalid item: {item}'))
                continue

            for field_name, field_value in fields.items():
                field = model._meta.get_field(field_name)
                if isinstance(field, (models.FileField, models.ImageField)):
                    new_file_path = self.copy_file_with_new_name(field_value)
                    fields[field_name] = new_file_path

            try:
                instance, created = model.objects.update_or_create(pk=pk, defaults=fields)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created instance with PK {pk}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated instance with PK {pk}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing item with PK {pk}: {e}'))

        # Clean up the extracted JSON file
        os.remove(json_file)

    def extract_json_from_zip(self, zip_file):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall('/tmp')  # Extract to a temporary directory
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.json'):
                        return os.path.join('/tmp', file_name)
        except zipfile.BadZipFile:
            raise CommandError(f'Error reading ZIP file "{zip_file}".')
        return None

    def copy_file_with_new_name(self, file_path):
        if not file_path:
            return file_path

        # Define the new file name
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        new_name = f"{name}_imported{ext}"
        new_path = os.path.join(os.path.dirname(file_path), new_name)

        # Check if default storage is S3
        if default_storage.__class__.__name__ == 'S3Boto3Storage':
            s3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

            copy_source = {
                'Bucket': bucket_name,
                'Key': file_path
            }

            try:
                s3_client.copy(copy_source, bucket_name, new_path)
                self.stdout.write(self.style.SUCCESS(f'Copied file to {new_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error copying file: {e}'))

        else:
            # Local storage case
            src = os.path.join(settings.MEDIA_ROOT, file_path)
            dst = os.path.join(settings.MEDIA_ROOT, new_path)
            shutil.copy(src, dst)

        return new_path
