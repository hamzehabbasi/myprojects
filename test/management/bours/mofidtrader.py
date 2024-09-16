# from telnetlib import EC
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import *
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def main():
    global nama
    driver = webdriver.Chrome()
    session_id= driver.session_id
    driver.get('https://account.emofid.com/login')
    time.sleep(5)

    # فیلد یوزرنیم
    element = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[1]/div[1]/input')
    ActionChains(driver).click(element).perform()
    time.sleep(3)
    element.send_keys('4060831360')
    time.sleep(3)

    #فیلد پسوورد
    passw = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[2]/div[1]/input')
    ActionChains(driver).click(passw).perform()
    time.sleep(2)
    passw.send_keys('591374Am')
    time.sleep(3)

    #کلیک روی دکمه ورود
    btn2 = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[3]/button')
    time.sleep(2)
    ActionChains(driver).click(btn2).perform()
    # easy= driver.find_element()
    time.sleep(3)

    #بازکردن میز کار حساب
    driver.get("https://m.easytrader.ir/")
    time.sleep(6)

    #ورود به دیده بان بازار
    view= driver.find_element(By.XPATH,'/html/body/app-root/div[1]/main-navbar/div/div/a[1]')
    ActionChains(driver).click(view).perform()
    time.sleep(5)

    # انتظار برای بارگذاری کامل صفحه
    driver.implicitly_wait(10)

    # گرفتن نماد بورسی مورد نظر از کاربر
    symbol = "کپارس"

    # پیدا کردن و کلیک کردن روی نماد بورسی
    try:
        # جستجوی نماد بورسی در بین لیست سهم‌ها
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        stock_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(symbol))

        for stock in stock_elements:
            list = []
            l = list.append(stock.text)
            if symbol in stock.text:
                stock.click()
                time.sleep(3)
                break
        else:
            print("نماد بورسی مورد نظر پیدا نشد.")

    except Exception as e:
        print(f"خطا در پیدا کردن یا کلیک کردن روی نماد بورسی: {e}")

    # SELECT BUY
    buy=driver.find_element(By.XPATH,'/html/body/app-root/div[1]/stock-details/div[2]/div/div/div[1]')
    ActionChains(driver).click(buy).perform()
    time.sleep(5)

    box_buy=driver.find_element(By.XPATH,
'/html/body/app-root/div[2]/overlay-management/order-form-container/div/div/div/order-form/form/div[1]/div/order-form-value2[1]/div/div[2]/custom-number-box/div/div/input')
    ActionChains(driver).click(box_buy).perform()
    time.sleep(3)

    # انتظار برای بارگذاری عنصر
    wait = WebDriverWait(driver, 10)

    #enter the number of symbel you want to buy

    number1 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                 '/html/body/app-root/div[2]/overlay-management/order-form-container/div/easy-keyboard/div/button[8]')))
    ActionChains(driver).click(number1).perform()

    wait = WebDriverWait(driver, 10)
    number2 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                 '/html/body/app-root/div[2]/overlay-management/order-form-container/div/easy-keyboard/div/button[8]')))
    ActionChains(driver).click(number2).perform()

    wait = WebDriverWait(driver, 10)
    number3 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                 '/html/body/app-root/div[2]/overlay-management/order-form-container/div/easy-keyboard/div/button[8]')))
    ActionChains(driver).click(number3).perform()

    wait = WebDriverWait(driver, 10)
    number4 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                 '/html/body/app-root/div[2]/overlay-management/order-form-container/div/easy-keyboard/div/button[8]')))
    # کلیک بر روی عنصر
    ActionChains(driver).click(number4).perform()

    wait = WebDriverWait(driver, 10)

    # finish the buying
    finish_buying=wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/div[2]/overlay-management/order-form-container/div/div/div/order-form/form/div[3]/button[1]')))
    ActionChains(driver).click(finish_buying).perform()

    time.sleep(700)
    driver.quit()


main()






#
# from selenium import webdriver
# from selenium.common import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
#
#
# def login(driver):
#     # driver.get('https://account.emofid.com/login')
#     # WebDriverWait(driver, 10).until(
#     #     EC.presence_of_element_located((By.XPATH, 'https://account.emofid.com/login"]'))
#     # )
#
#     global nama
#     # driver = webdriver.Chrome()
#     session_id= driver.session_id
#     driver.get('https://account.emofid.com/login')
#     time.sleep(5)
#
#     # فیلد یوزرنیم
#     username_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[1]/div[1]/input')
#     # username_field = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
#     username_field.send_keys('4060831360')
#
#     # فیلد پسوورد
#     password_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[2]/div[1]/input')
#     ActionChains(driver).click(password_field).perform()
#     time.sleep(2)
#     password_field.send_keys('591374Am')
#     time.sleep(3)
#     # password_field = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
#     # password_field.send_keys('591374Am')
#
#     # کلیک روی دکمه ادامه
#     # login_button = driver.find_element(By.XPATH, '//button[text()="Continue"]')
#     # login_button.click()
#     btn2 = driver.find_element(By.XPATH,'/html/body/div/div/div/div/div[1]/div[1]/div/form/fieldset/div[3]/button')
#     time.sleep(2)
#     ActionChains(driver).click(btn2).perform()
#     # easy= driver.find_element()
#     time.sleep(5)
#
# def open_easy_trader(driver):
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//a[@class="btn btn-info btn-block d-md-none"]'))
#     )
#     driver.get("https://m.easytrader.ir/")
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//a[text()="دیده‌بان"]'))
#     )
#     watchlist_button = driver.find_element(By.XPATH, '//a[text()="دیده‌بان"]')
#     watchlist_button.click()
#
#
# def get_namadha(driver):
#     try:
#         WebDriverWait(driver, 20).until(
#             EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.ag-cell-value'))
#         )
#         source = driver.page_source
#         soup = BeautifulSoup(source, 'html.parser')
#         namadha = [nm.text.strip() for nm in soup.select('span.ag-cell-value')]
#         print(f'namadha: {namadha}')
#         return namadha
#     except TimeoutException:
#         print("TimeoutException: Unable to locate elements.")
#         return []
#
# def click_on_name(driver, name):
#     try:
#         element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, f'//app-symbol-state-renderer[contains(text(),"{name}")]'))
#         )
#         element.click()
#     except TimeoutException:
#         print(f"TimeoutException: Element with name '{name}' not found.")
#
#
# # تابع اصلی
# def main():
#     driver = webdriver.Chrome()
#     try:
#         login(driver)
#         open_easy_trader(driver)
#         namadha = get_namadha(driver)
#         print(f'namadha: {namadha}')
#
#         name = 'خودرو'
#         if name in namadha:
#             click_on_name(driver, name)
#
#         time.sleep(300)  # Keep the browser open for 5 minutes
#     finally:
#         driver.quit()
#
#
# if __name__ == "__main__":
#     main()

# main()