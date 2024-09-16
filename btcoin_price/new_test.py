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


# دریافت پیام‌های کانال تلگرام به صورت async

async def get_channel_messages(offset=None):
    bot_token = '7316797697:AAEkspaYR33gMF6J9PCRD3rI6aY_qKS0agI'  # توکن ربات را بررسی کنید
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    params = {}
    if offset:
        params['offset'] = offset

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if 'result' in data:
                    messages = [msg['channel_post'] for msg in data['result'] if 'channel_post' in msg]
                    if messages:
                        new_offset = data['result'][-1]['update_id'] + 1
                        return messages, new_offset
                    else:
                        return [], offset
                else:
                    print(f"No result found in response: {data}")
                    return [], offset
            else:
                # چاپ پیام خطا با جزئیات بیشتر
                error_text = await response.text()
                print(f"Error fetching messages, status code: {response.status}, response: {error_text}")
                return [], offset


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
    bot_token = '7153246534:AAEK4ka2OPOfZSc2tSAqCQj--EQvWIC9VS0'
    chat_id = '@btconehondred'
    notification_chat_id = '@get_messages1'
    message_count = 1
    down_count = 0
    final_count = 4
    previous_price = None
    threshold = 100
    messages = []
    while True:
        try:
            current_price = await get_bitcoin_price()
            if current_price is None:
                await asyncio.sleep(5)
                continue

            # بررسی تغییرات قیمت
            if previous_price is not None:
                price_difference = current_price - previous_price
                if abs(price_difference) >= threshold:
                    if current_price > previous_price:
                        message = f" {message_count} : BTC-price: {current_price} USD - UP"
                    else:
                        message = f"{message_count} : BTC-price: {current_price} USD - DOWN"
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

                if "UP" in last_message and "UP" in fifth_last_message:
                    similar_message = f"BTCUSDT up number : {last_message_count} - {fifth_last_message_count} "
                    await send_to_telegram_async(bot_token, chat_id, similar_message)
                    down_count += 1

                elif "DOWN" in last_message and "DOWN" in fifth_last_message:

                    similar_message = f"BTCUSDT down number : {last_message_count} - {fifth_last_message_count} "
                    await send_to_telegram_async(bot_token, chat_id, similar_message)
                    down_count += 1

                elif ("UP" in last_message and "DOWN" in fifth_last_message) or (
                        "DOWN" in last_message and "UP" in fifth_last_message):
                    continue

                if down_count >= final_count:
                    final_message = f"شرایط محقق شد: 4 پیام پشت سر هم 'DOWN' or  UP."
                    await send_to_telegram_async(bot_token, notification_chat_id, final_message)
                    down_count = 0

            await asyncio.sleep(0.5)  # تاخیر کوتاه بین هر حلقه

        except Exception as e:
            print(f"خطا رخ داد: {e}")
            await asyncio.sleep(5)


# اجرای main به صورت async
if __name__ == "__main__":
    asyncio.run(main())
