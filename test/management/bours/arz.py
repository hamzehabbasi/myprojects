from pycoingecko import CoinGeckoAPI
import json
from bs4 import BeautifulSoup
import requests

url= requests.get('https://www.tgju.org/profile/price_dollar_rl')
soup = BeautifulSoup(url.text,'html.parser')
dollar=soup.find('td',attrs={'class':'nf'})
price = int(dollar.text.replace(',', ''))

cg=CoinGeckoAPI()
bitcoin=cg.get_price(ids='etheium',vs_currencies='usd')
print(bitcoin)