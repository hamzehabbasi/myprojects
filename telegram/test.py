import json  # اضافه کردن کتابخانه json
import requests
from bs4 import BeautifulSoup


# تابع برای دریافت قیمت نماد
def get_stock_price(symbol):
    url = 'https://www.estjt.ir/'  # URL سایت مورد نظر
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # جستجو برای نماد و قیمت
    stock_element = soup.find(text=symbol)
    if stock_element:
        price_element = stock_element.find_next('td')  # یافتن عنصر بعدی که ممکن است قیمت باشد
        stock_price = price_element.text.strip() if price_element else "قیمت پیدا نشد"
        return stock_price
    else:
        return "نماد مورد نظر پیدا نشد."


# تابع برای ذخیره دیکشنری شامل نمادها و قیمت‌ها در فایل JSON
def save_prices_to_json(symbol_price_dict):
    try:
        with open('j.json', 'w', encoding='utf-8') as file:
            json.dump(symbol_price_dict, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"خطا در ذخیره‌سازی فایل JSON: {e}")


symbols = ["انس طلا", "مظنه تهران", "طلا ۱۸ عیار", "طلا ۲۴ عیار", "سکه طرح جدید", "سکه طرح قدیم", "نیم سکه",
           "ربع سکه", "سکه گرمی"]

# ساخت دیکشنری برای نمادها و قیمت‌ها
symbol_price_dict = {}

for symbol in symbols:
    stock_price = get_stock_price(symbol)
    symbol_price_dict[symbol] = stock_price
    print(f'stock:{stock_price}')

# ذخیره دیکشنری در فایل JSON
save_prices_to_json(symbol_price_dict)

# نمایش دیکشنری نهایی
print(symbol_price_dict)
