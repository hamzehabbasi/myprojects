# import telebot
# from telegram import Update
# from telegram.ext import *
#
# from telegram import Update
# from telegram.ext import Application, CommandHandler, ContextTypes
#
# from telegram_bot import bot
#
# # توکن API که از BotFather دریافت کرده‌اید
# # API_TOKEN = '6718051921:AAFiblrJVXtL99WA4BtIC8y62QiQARWbMlc'
# bot = telebot.TeleBot("6718051921:AAFiblrJVXtL99WA4BtIC8y62QiQARWbMlc")
#
# # برای ذخیره لینک
# group_link = 'http://t.me/Mem1_Add1_bot'
#
# @bot.message_handler(commands=["start"])
#
# # تابع برای دستور /start
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text("سلام! لطفاً لینک گروه خود را با دستور /setlink ارسال کنید.")
#
# # تابع برای دریافت و ذخیره لینک گروه
# async def set_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     global group_link
#     if context.args:
#         group_link = context.args[0]
#         await update.message.reply_text(f"لینک گروه با موفقیت ذخیره شد:\n{group_link}")
#     else:
#         await update.message.reply_text("لطفاً لینک گروه را پس از دستور /setlink وارد کنید.")
#
# # تابع برای ارسال لینک ذخیره شده به کاربران
# async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     if group_link:
#         await update.message.reply_text(f"لینک گروه:\n{group_link}")
#     else:
#         await update.message.reply_text("هنوز هیچ لینکی ذخیره نشده است. لطفاً از دستور /setlink استفاده کنید.")
#
# def main() -> None:
#     # ایجاد شیء Application
#     application = Application.builder().token(API_TOKEN).build()
#
#     # تعریف handlerها برای دستورات
#     start_handler = CommandHandler('start', start)
#     setlink_handler = CommandHandler('setlink', set_link)
#     getlink_handler = CommandHandler('getlink', get_link)
#
#     # افزودن handlerها به application
#     application.add_handler(start_handler)
#     application.add_handler(setlink_handler)
#     application.add_handler(getlink_handler)
#
#     # شروع ربات
#     application.run_polling()
#
# if __name__ == '__main__':
#     main()

import requests
from bs4 import BeautifulSoup

def get_stock_price(symbol):
    url = 'https://www.estjt.ir/'  # URL سایت مورد نظر
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # جستجو برای نماد و قیمت
    stock_element = soup.find(text=symbol)
    if stock_element:
        price_element = stock_element.find_next('td')  # یافتن عنصر بعدی که ممکن است قیمت باشد
        stock_price = price_element.text if price_element else "قیمت پیدا نشد"
        return stock_price
    else:
        return "نماد مورد نظر پیدا نشد."

symbols=["انس طلا", "مظنه تهران", "طلا ۱۸ عیار", "طلا ۲۴ عیار", "سکه طرح جدید", "سکه طرح قدیم", "نیم سکه",
         "ربع سکه", "سکه گرمی"]

for symbol in symbols:
    # d=symbol
    f=get_stock_price(symbol)
    print(f'fffff{f}')