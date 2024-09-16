#
# برای بک‌آپ‌گیری از دیتابیس محلی و انتقال آن به سرور آنلاین، می‌توانید از دستورات `manage.py` در Django و ابزارهای سیستم‌عامل مانند `scp` (Secure Copy) استفاده کنید. در اینجا یک نمونه کد برای این کار آورده شده است:
#
# 1. **بک‌آپ گرفتن از دیتابیس محلی:**
#
# ابتدا یک کامند در Django ایجاد می‌کنیم تا دیتابیس محلی را بک‌آپ بگیرد.
#
# ```python
# # commands/backup_db.py
# from django.core.management.base import BaseCommand
# from django.conf import settings
# import os
# import subprocess
#
# class Command(BaseCommand):
#     help = 'Backup local database'
#
#     def handle(self, *args, **kwargs):
#         db_name = settings.DATABASES['default']['NAME']
#         db_user = settings.DATABASES['default']['USER']
#         db_password = settings.DATABASES['default']['PASSWORD']
#         db_host = settings.DATABASES['default']['HOST']
#         db_port = settings.DATABASES['default']['PORT']
#
#         backup_file = f'{db_name}.sql'
#         dump_command = f'pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name} > {backup_file}'
#
#         env = os.environ.copy()
#         env['PGPASSWORD'] = db_password
#
#         subprocess.run(dump_command, shell=True, env=env)
#         self.stdout.write(self.style.SUCCESS(f'Database backup successful: {backup_file}'))
# ```
#
# این کد برای بک‌آپ گرفتن از دیتابیس PostgreSQL است. اگر از دیتابیس دیگری استفاده می‌کنید، دستور مناسب را در `dump_command` قرار دهید.
#
# 2. **انتقال بک‌آپ به سرور آنلاین:**
#
# پس از ایجاد بک‌آپ، باید فایل بک‌آپ را به سرور آنلاین انتقال دهید. می‌توانید از `scp` استفاده کنید.
#
# ```python
# # commands/upload_backup.py
# from django.core.management.base import BaseCommand
# import subprocess
#
# class Command(BaseCommand):
#     help = 'Upload database backup to remote server'
#
#     def add_arguments(self, parser):
#         parser.add_argument('backup_file', type=str, help='Path to the backup file')
#         parser.add_argument('remote_user', type=str, help='Remote server username')
#         parser.add_argument('remote_host', type=str, help='Remote server host')
#         parser.add_argument('remote_path', type=str, help='Remote server path')
#
#     def handle(self, *args, **kwargs):
#         backup_file = kwargs['backup_file']
#         remote_user = kwargs['remote_user']
#         remote_host = kwargs['remote_host']
#         remote_path = kwargs['remote_path']
#
#         scp_command = f'scp {backup_file} {remote_user}@{remote_host}:{remote_path}'
#         subprocess.run(scp_command, shell=True)
#         self.stdout.write(self.style.SUCCESS(f'Backup file uploaded to {remote_host}:{remote_path}'))
# ```
#
# 3. **استفاده از کامندها:**
#
# ابتدا بک‌آپ بگیرید و سپس آن را به سرور آنلاین انتقال دهید.
#
# ```sh
# python manage.py backup_db
# python manage.py upload_backup <backup_file> <remote_user> <remote_host> <remote_path>
# ```
#
# این دستورها به ترتیب بک‌آپ را می‌گیرند و آن را به سرور آنلاین منتقل می‌کنند.
#
# ### نکات مهم:
# 1. برای امنیت بیشتر، اطمینان حاصل کنید که فایل‌های بک‌آپ را پس از انتقال پاک کنید.
# 2. دسترسی‌های مناسب برای اجرای دستورات `pg_dump` و `scp` را فراهم کنید.
# 3. در صورت نیاز، از SSH key برای اتصال امن به سرور آنلاین استفاده کنید.