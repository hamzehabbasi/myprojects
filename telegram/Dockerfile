# # انتخاب تصویر پایه
# FROM python:3.8-slim
#
# # تنظیم دایرکتوری کاری در کانتینر
# WORKDIR /app
#
# # کپی کردن فایل‌های پروژه به دایرکتوری کاری
# COPY . /app
#
# # نصب وابستگی‌ها از فایل requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
#
# # فرمان پیش‌فرض برای اجرای برنامه
# CMD ["python", "gold_rate_telegram_bot.py"]


FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install build-essential -y

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "gold_rate_telegram_bot.py"]
