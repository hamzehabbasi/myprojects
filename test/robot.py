
import alpaca_trade_api as tradeapi

# SEC_KEY = '' # Enter Your Secret Key Here
#
# PUB_KEY = '' # Enter Your Public Key Her
# BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
# api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL) # For real trading, don’t enter a base_url
#
# # Buy a stock
# api.submit_order(
#     symbol='SPY', # Replace with the ticker of the stock you want to buy
#     qty= 1,
#     side= 'buy',
#     type= 'market',
#     time_in_force= 'gtc' # Good ’til cancelled
#     )
#
# # Sell a stock(Just change side to ‘sell’)
# api.submit_order(
#     symbol='SPY',
#     qty=1,
#     side= 'sell',
#     type= 'market',
#     time_in_force= 'gtc'
#     )


import requests

url = "https://data.alpaca.markets/v1beta1/forex/latest/rates"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)


