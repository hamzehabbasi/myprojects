# import requests
# import time
# import random
#
#
# # تابع دریافت قیمت بیتکوین از API
# def bitcoin_price():
#     url = 'https://api.wallex.ir/v1/currencies/stats'
#
#     # افزودن پارامتر تصادفی به URL برای جلوگیری از کش شدن درخواست‌ها
#     params = {'nocache': random.random()}
#
#     # تنظیم هدرهای مناسب برای جلوگیری از کش شدن
#     headers = {
#         'Cache-Control': 'no-cache',
#         'Pragma': 'no-cache'
#     }
#
#     response = requests.get(url, params=params, headers=headers)
#
#     if response.status_code == 200:
#         data = response.json()
#         if data.get('success'):
#             currencies = data.get('result', [])
#             for currency in currencies:
#                 if currency['key'] == 'BTC':
#                     return currency['price']
#         else:
#             print("خطا در دریافت اطلاعات: ", data.get('message'))
#     else:
#         print(f"خطا در ارتباط با سرور. وضعیت: {response.status_code}")
#
#     return None
#
#
# # حلقه اصلی برای ارسال درخواست به API هر ۵ ثانیه
# def main():
#     while True:
#         price = bitcoin_price()
#         if price is not None:
#             print(f"قیمت بیتکوین: {price} USDT")
#         else:
#             print("عدم توانایی در دریافت قیمت")
#
#         time.sleep(5)  # وقفه ۵ ثانیه‌ای بین هر درخواست
#
#
# # اجرای برنامه
# if __name__ == "__main__":
#     main()
#
# import requests
# import time
# import telebot
#
#
# # تابع اتصال به API نوبیتکس
# def nobitex_connect(uri=None, token=None, method='post', data=None):
#     url = 'https://api.nobitex.ir/'
#     headers = {}
#     if uri:
#         url += uri
#     if token:
#         headers = {'Authorization': token}
#     if method == 'post':
#         if data:
#             r = requests.post(url, headers=headers, data=data)
#         else:
#             r = requests.post(url, headers=headers)
#     else:
#         if data:
#             r = requests.post(url, headers=headers, data=data)
#         else:
#             r = requests.get(url, headers=headers)
#     return r.status_code, r.json()
#
#
# # دریافت آخرین قیمت بیتکوین
# def orderbook():
#     symbol = 'BTCUSDT'
#     price = nobitex_connect(uri=f'v2/orderbook/{symbol}', method='get')
#     return price[1]['lastTradePrice']
#
#
# # حلقه اصلی برای ارسال درخواست به API هر ۵ ثانیه
# def main():
#     while True:
#         price = orderbook()
#         if price is not None:
#             print(f"قیمت بیتکوین: {price} USDT")
#         else:
#             print("عدم توانایی در دریافت قیمت")
#
#         time.sleep(5)  # وقفه ۵ ثانیه‌ای بین هر درخواست
#
#
# # اجرای برنامه
# if __name__ == "__main__":
#     main()
# e=orderbook()
# print(e)


import requests


def get_bitcoin_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data['price']
        return float(price)
    else:
        return "Error fetching price"


price = get_bitcoin_price()
print(f"The current price of Bitcoin (BTC) is: ${price}")


response:<Response [451]>
این پیام در ریکویستی که به بایننس میزنیم یعنی چه