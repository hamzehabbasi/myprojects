import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import *

# driver = webdriver.Chrome()

# driver.get('https://akharinkhabar.ir/')
#
# source = driver.page_source
# soup = BeautifulSoup(source, 'html.parser')
# text = []
#
# for nm in soup.select('body'):
#     e=text.append(nm.text.strip())
#     print(f'text: {e}')
# print(f'soup: {soup}')
# time.sleep(400)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# نصب و راه‌اندازی کروم درایور
driver = webdriver.Chrome()

# باز کردن صفحه دیده‌بان بازار
driver.get("https://alirezamehrabi.com/saham/list")


# انتظار برای بارگذاری کامل صفحه
driver.implicitly_wait(10)

# گرفتن نماد بورسی مورد نظر از کاربر
symbol = input("enter your symbol:")

# پیدا کردن و کلیک کردن روی نماد بورسی
try:
    # جستجوی نماد بورسی در بین لیست سهم‌ها
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    stock_elements = driver.find_elements(By.XPATH,"//*[contains(text(), '{}')]".format(symbol))

    for stock in stock_elements:
        list=[]
        l=list.append(stock.text)
        if symbol in stock.text:
            stock.click()
            break
    else:
        print("نماد بورسی مورد نظر پیدا نشد.")

except Exception as e:
    print(f"خطا در پیدا کردن یا کلیک کردن روی نماد بورسی: {e}")

# صبر برای مشاهده نتایج (اختیاری)
time.sleep(190)

# بستن مرورگر
driver.quit()

