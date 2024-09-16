
import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup

# توکن ربات تلگرام خود را اینجا قرار دهید
TOKEN = '7153246534:AAEK4ka2OPOfZSc2tSAqCQj--EQvWIC9VS0'
bot = telebot.TeleBot(TOKEN)

# تابع برای ذخیره دیکشنری شامل نمادها و قیمت‌ها در فایل JSON
def save_prices_to_json(symbol_price_dict):
    try:
        with open('j.json', 'w', encoding='utf-8') as file:
            json.dump(symbol_price_dict, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"خطا در ذخیره‌سازی فایل JSON: {e}")

# تابع برای بارگذاری قیمت‌ها از فایل JSON
def load_prices_from_json():
    try:
        with open('j.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}  # اگر فایل JSON وجود نداشته باشد، دیکشنری خالی برمی‌گردد

# تابع برای دریافت قیمت نماد و ذخیره در فایل JSON (در صورت نیاز)
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

# تابع شروع برای نمایش دکمه‌ها
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    buttons = [
        InlineKeyboardButton("انس طلا", callback_data='انس طلا'),
        InlineKeyboardButton("مظنه تهران", callback_data='مظنه تهران'),
        InlineKeyboardButton("طلا ۱۸ عیار", callback_data='طلا ۱۸ عیار'),
        InlineKeyboardButton("طلا ۲۴ عیار", callback_data='طلا ۲۴ عیار'),
        InlineKeyboardButton("سکه طرح جدید", callback_data='سکه طرح جدید'),
        InlineKeyboardButton("سکه طرح قدیم", callback_data='سکه طرح قدیم'),
        InlineKeyboardButton("نیم سکه", callback_data='نیم سکه'),
        InlineKeyboardButton("ربع سکه", callback_data='ربع سکه'),
        InlineKeyboardButton("سکه گرمی", callback_data='سکه گرمی')
    ]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'لطفاً یک نماد را انتخاب کنید:', reply_markup=keyboard)

# تابع مدیریت کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "در حال دریافت قیمت...")

    # بارگذاری داده‌های موجود از فایل JSON
    symbol_prices = load_prices_from_json()

    # بررسی اینکه آیا قیمت نماد در فایل JSON موجود است یا خیر
    stock_price = symbol_prices.get(call.data, "قیمت موجود نیست. لطفاً دوباره تلاش کنید.")

    # ارسال نتیجه به کاربر
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{call.data} - قیمت: {stock_price}")

# شروع به کار ربات
if __name__ == '__main__':
    print("Bot is polling...")
    bot.polling()
