import requests
import pandas as pd

# آدرس API سایت بورس ایران (مثال)
api_url = 'http://tsetmc.com/tsev2/data/InstTradeHistory.aspx?i=46348559193224090&Top=9999&A=1'

# ارسال درخواست به API
response = requests.get(api_url)
print(f'response:{response}')
# بررسی وضعیت پاسخ
if response.status_code == 200:
    data = response.text
    print(f'data: {data}')  # داده‌های خام دریافتی را نمایش می‌دهد

    # پردازش داده‌ها (در اینجا فرض شده داده‌ها CSV هستند)
    data_lines = data.split(';')
    processed_data = [line.split(',') for line in data_lines if line]

    # تبدیل به DataFrame برای سهولت در استفاده
    df = pd.DataFrame(processed_data, columns=['Date', 'High', 'Low', 'Close', 'Value', 'Volume', 'Number of Trades'])

    # نمایش داده‌ها
    print(df)
else:
    print("خطا در دریافت داده‌ها:", response.status_code)
