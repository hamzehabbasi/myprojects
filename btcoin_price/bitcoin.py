import aiohttp
import asyncio
import time


# دریافت قیمت بیتکوین از بایننس به صورت async
async def get_bitcoin_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                price = data['price']
                return float(price)
            else:
                print("Error fetching price from Binance")
                return None


# async def get_bitcoin_price():
#     url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
#     prices = []
#
#     async with aiohttp.ClientSession() as session:
#         for _ in range(5):  # 5 درخواست در هر ثانیه
#             async with session.get(url) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     price = float(data['price'])
#                     prices.append(price)  # ذخیره قیمت دریافت شده
#                 else:
#                     print(f"Error fetching price from Binance: {response.status}")
#
#                 # خواب کوتاه برای اینکه درخواست‌ها با فاصله کوتاه ارسال شوند (0.2 ثانیه برای 5 درخواست در هر ثانیه)
#                 await asyncio.sleep(0.1)
#
#     return prices  # بازگرداندن لیست قیمت‌ها


# دریافت پیام‌های کانال تلگرام به صورت async

# async def get_channel_messages(offset=None):
#     bot_token = '7316797697:AAEkspaYR33gMF6J9PCRD3rI6aY_qKS0agI'  # توکن ربات را بررسی کنید
#     url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
#
#     params = {}
#     if offset:
#         params['offset'] = offset
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, params=params) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 if 'result' in data:
#                     messages = [msg['channel_post'] for msg in data['result'] if 'channel_post' in msg]
#                     if messages:
#                         new_offset = data['result'][-1]['update_id'] + 1
#                         return messages, new_offset
#                     else:
#                         return [], offset
#                 else:
#                     print(f"No result found in response: {data}")
#                     return [], offset
#             else:
#                 # چاپ پیام خطا با جزئیات بیشتر
#                 error_text = await response.text()
#                 print(f"Error fetching messages, status code: {response.status}, response: {error_text}")
#                 return [], offset
#

# ارسال پیام به تلگرام به صورت async
async def send_to_telegram_async(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=params) as response:
            if response.status == 200:
                print("پیام با موفقیت ارسال شد")
            else:
                print(f"Error sending message, status code: {response.status}")


# حلقه اصلی برای به‌روزرسانی قیمت بیت‌کوین و بررسی پیام‌های تلگرام
async def main():
    bot_token = '7390882203:AAFap8oDw5Ole-dfmX46jZe6oN8Z6zzxmPo'
    chat_id = '@bitcoinusdtup'
    notification_chat_id = '@get_message_updown'
    message_count = 1
    down_count = 0
    final_count = 4
    previous_price = None
    threshold = 100
    messages = []
    up_down_for_another_chanel = []
    while True:
        try:
            current_price = await get_bitcoin_price()
            # for current_price in current_prices:
            if current_price is None:
                await asyncio.sleep(5)
                continue

                # بررسی تغییرات قیمت
            if previous_price is not None:
                price_difference = current_price - previous_price
                if abs(price_difference) >= threshold:
                    if current_price > previous_price:
                        message = f" {message_count} : BTC-price: {current_price} - UP"
                    else:
                        message = f"{message_count} : BTC-price: {current_price} - DOWN"
                    await send_to_telegram_async(bot_token, chat_id, message)
                    message_count += 1

                    message = message.split()
                    messages.append(message)

                elif abs(price_difference) > threshold + 3 or abs(price_difference) < threshold:
                    continue

            previous_price = current_price

            # دریافت پیام‌های تلگرام

            if len(messages) > 5:
                messages.pop(0)
            # مقایسه پیام آخر با پنجمین پیام قبل
            if len(messages) == 5:
                last_message = messages[-1]
                fifth_last_message = messages[-5]
                last_message_count = last_message[0]
                fifth_last_message_count = fifth_last_message[0]
                up_down = last_message[-1]

                if "UP" in last_message and "UP" in fifth_last_message:
                    similar_message = f"btcusdt (up) number : {last_message_count} - {fifth_last_message_count} "
                    await send_to_telegram_async(bot_token, chat_id, similar_message)
                    up_down_for_another_chanel.append(up_down)
                    down_count += 1
                    if down_count > 2:
                        sum_number = f"number : {down_count}"
                        await send_to_telegram_async(bot_token, chat_id, sum_number)

                elif "DOWN" in last_message and "DOWN" in fifth_last_message:
                    similar_message = f"btcusdt (down) number : {last_message_count} - {fifth_last_message_count} "
                    await send_to_telegram_async(bot_token, chat_id, similar_message)
                    up_down_for_another_chanel.append(up_down)
                    down_count += 1
                    if down_count > 2:
                        sum_number = f"number : {down_count}"
                        await send_to_telegram_async(bot_token, chat_id, sum_number)

                elif ("UP" in last_message and "DOWN" in fifth_last_message) or (
                        "DOWN" in last_message and "UP" in fifth_last_message):
                    down_count = 0
                    up_down_for_another_chanel = []

                if down_count == final_count:
                    final_message = f"number : 1-4 : {up_down_for_another_chanel}"
                    await send_to_telegram_async(bot_token, notification_chat_id, final_message)

                elif down_count > final_count:
                    final_message = f'number: {down_count} : {up_down_for_another_chanel}'
                    await send_to_telegram_async(bot_token, notification_chat_id, final_message)

            await asyncio.sleep(0.2)  # تاخیر کوتاه بین هر حلقه

        except Exception as e:
            print(f"خطا رخ داد: {e}")
            await asyncio.sleep(5)


# اجرای main به صورت async
if __name__ == "__main__":
    asyncio.run(main())
