list_symbol=[
    'BTCIRT', 'ETHIRT', 'LTCIRT', 'USDTIRT', 'XRPIRT', 'BCHIRT', 'BNBIRT', 'EOSIRT', 'XLMIRT',
    'ETCIRT', 'TRXIRT', 'DOGEIRT', 'UNIIRT', 'DAIIRT', 'LINKIRT', 'DOTIRT', 'AAVEIRT', 'ADAIRT',
    'SHIBIRT', 'FTMIRT', 'MATICIRT', 'AXSIRT', 'MANAIRT', 'SANDIRT', 'AVAXIRT', 'MKRIRT', 'GMTIRT',
    'USDCIRT', 'BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'XRPUSDT', 'BCHUSDT', 'BNBUSDT', 'EOSUSDT', 'XLMUSDT',
    'ETCUSDT', 'TRXUSDT', 'PMNUSDT', 'DOGEUSDT', 'UNIUSDT', 'DAIUSDT', 'LINKUSDT', 'DOTUSDT', 'AAVEUSDT',
    'ADAUSDT', 'SHIBUSDT', 'FTMUSDT', 'MATICUSDT','AXSUSDT', 'MANAUSDT', 'SANDUSDT', 'AVAXUSDT', 'MKRUSDT',
    'GMTUSDT', 'USDCUSDT']
currency=[
    'rls', 'btc', 'eth', 'ltc', 'usdt', 'xrp', 'bch', 'bnb', 'eos', 'xlm', 'etc',
    'trx', 'pmn', 'doge', 'uni', 'dai', 'link', 'dot', 'aave', 'ada', 'shib',
    'ftm', 'matic', 'axs', 'mana', 'sand', 'avax', 'mkr', 'gmt', 'usdc'
]
import requests

body_asli = {'token': 'token 743fa839a9cc55cf2d65463b5ce535545559b9bf','symbol':'BTCUSDT','symbol_dif':'btc',
              'bank':'تجارت','card_bank':'58483949292'}

def nobitex_connect(uri=None, token=None, method='post',data=None):
    url = 'https://api.nobitex.ir/'
    headers = {}
    if uri:
        url += uri
    if token:
        headers = {'Authorization': token}
    if method == 'post':
        if data:
            r=requests.post(url,headers=headers, data= data)
        else:
            r = requests.post(url, headers=headers)
    else:
        if data:
            r = requests.post(url, headers=headers, data=data)
        else:
            r = requests.get(url, headers=headers)
    return r.status_code, r.json()

# 1
def orderbook(body):
        symbol = body['symbol']
        return nobitex_connect(uri=f'v2/orderbook/{symbol}', method='get')
# o=orderbook(body_asli)
# print(o)


# 2
def deep_chart(body):
        symbol = body['symbol']
        return nobitex_connect(uri=f'v2/orderbook/{symbol}', method='get')
# n = deep_chart(body_asli)
# print(n)

# 3
def trade_list(body):
        symbol = body['symbol']
        return nobitex_connect(uri=f'v2/trades/{symbol}', method='get')
# t= trade_list(body_asli)
# print(t)

# 4
def nobitex_market_state(body):
    token = body['token']
    symbol_dif=body['symbol_dif']
    return nobitex_connect(uri=f'market/stats?srcCurrency={symbol_dif}&dstCurrency={symbol_dif}',token=token,method='get')
# s = nobitex_market_state(body_asli)
# print(s)

# 5
def ohlc(body):
    symbol = body['symbol']
    token = body['token']
    return nobitex_connect(uri=f'market/udf/history?symbol={symbol}&resolution=D&from=1562058167&to=1562230967',token=token,method='get')
# o = ohlc(body_asli)
# print(o)

# 6
def global_states(body):
        token = body['token']
        return nobitex_connect(uri=f'market/global-stats',token=token,method='post')
# g= global_states(body_asli)
# print(g)

# 7
def customer_profile(body):
    token=body['token']
    return nobitex_connect(uri='users/profile', token=token, method='get')
# u=customer_profile(body_asli)
# print(f'customer_ profile{u}')

# 8
def blockchain_address_create(body):
    token=body['token']
    data={'currency':body['symbol_dif']}
    return nobitex_connect(uri='users/wallets/generate-address', token=token, method='get',data=data)
# u=blockchain_address_create(body_asli)
# print(f'blockchain_address_create{u}')

# 9
def bank_cards_add(body):
    token=body['token']
    data={'number':body['card_bank'],'bank':body['bank']}
    return nobitex_connect(uri='users/cards-add', token=token, method='post',data=data)
# u=bank_cards_add(body_asli)
# print(f'bank_cards_add{u}')

# 10
def wallet_lists_selective(body):
    token=body['token']
    symbol_dif=body['symbol_dif']
    return nobitex_connect(uri=f'v2/wallets?currencies=usdt,{symbol_dif}', token=token, method='get')
u=wallet_lists_selective(body_asli)
print(f'user restrictions:{u}')

# 11
def wallet_list(body):
    token=body['token']
    return nobitex_connect(uri='users/wallets/list', token=token, method='get')
w=wallet_list(body_asli)
print(w)

# 12
def favorite_market(body):
    token=body['token']
    return nobitex_connect(uri='users/markets/favorite', token=token, method='get')
# f=favorite_market(body_asli)
# print(f)

# 13
def user_restrictions(body):
    token=body['token']
    return nobitex_connect(uri='users/limitations', token=token, method='get')
# cm=customer_mahdodyyat(body_asli)
# print(f'customer_mahdodyyat{cm}')

# 14
# def wallet_transactions_list():
#     wtl=requests.get('https://api.nobitex.ir/users/wallets/transactions/list?wallet=4159',
#                     headers={'Authorization':'token 743fa839a9cc55cf2d65463b5ce535545559b9bf'})
#     return wtl.status_code, wtl.json()
# wtl=wallet_transactions_list()
# print(f'wallet_transactions_list: {wtl}')

# 15
def wallet_deposit_list(body):
    token=body['token']
    return nobitex_connect(uri='users/wallets/deposits/list?wallet=4159', token=token, method='post')
# wb=wallet_deposit_list(body_asli)
# print(f'wallet_deposit_list: {wb}')


# 17
def add_ordders():
    ao=requests.post('https://api.nobitex.ir/margin/orders/add',headers={'Authorization':'token 743fa839a9cc55cf2d65463b5ce535545559b9bf',
                                                                        "content-type": "application/json"},
                    data= {"srcCurrency": "btc", "dstCurrency": "rls", "leverage": "2", "amount": "0.9", "price": "6400000000"})
    return ao.status_code,ao.json()
# a=add_ordders()
# print(f'asdsd:{a}')


    # import matplotlib.pyplot as plt
# # x axis values
# x = [1,2,3,4]
# # corresponding y axis values
# y = [2,4,1,8]
# # plotting the points
# plt.plot(x, y)
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
# # giving a title to my graph
# plt.title('My first graph!')
# # function to show the plot
# plt.show()
#
# left = [1, 2, 3, 4, 5]
# # heights of bars
# height = [10, 20, 30, 40, 100]
# # labels for bars
# tick_label = ['one', 'two', 'three', 'four', 'five']
# # plotting a bar chart
# plt.bar(left, height, tick_label = tick_label,
#         width = 0.8, color = ['blue', 'green', 'red','yellow','black'])
# # naming the x-axis
# plt.xlabel('x - axis')
# # naming the y-axis
# plt.ylabel('y - axis')
# # plot title
# plt.title('bar chart!')
# # function to show the plot
# # plt.show()
