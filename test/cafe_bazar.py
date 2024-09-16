
# tokens:{'access_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQyOTk2ODYsInVzZXJfaWQiOjYyMzU4OTMxLCJzY29wZXMiOlsiYW5kcm9pZHB1Ymxpc2hlciJdfQ.Os3Rrp56Cyzkx30TNME2A8LIJOCkrXFUwu5NiC63NlTMs1zEQA83_4VNiH_6njj0bzaRQRYstTRUCqsQSzsVeJY8f6ZufeJleydHnoq4EWezona_ufW-Ez1u_KcA7lCI35Lustvq9f1hllOcD9KhAB4LIDjY5bbO3nS1iFWly9M1fZvmlxoC1R4DgUutX2izPuZ2kkq8AfA9ovknXlHN653vyYghQCuEPEbqb182jTVCUv7QmxUOEL0b7h9BIqz9EWb7wqgRSt66e6lUWkcdkcypU4MLEQAh6XC_cS798vOEBo3LB3JicgRdiHWfmek-cyp0k1qHG5Tv1EHHkRFNYoyZm_QrO8_cm2HCUZUN8i7kv51MUK09_rITcMB8odHH40h7W-it_H-8p1xoYwOie3dMyvZEGhE_kQa04O7EKiC0SluzlffYWbkYP2AFFeJAi9Hfa_Ot7hcBagiE98OjIePN8iPD6zaKGVxS0TkGLdXYrx2w02Tcoe3w1pQcCVzY7VkHSSZXxjna2TB1f2ebiOnebCD0ZSyupZpu0TK5Uat88wp1zBUz9VRvFDsGIZr663ujLfR2maeaQEdROKrmP1kvYGXbHY3CvWet8tqbR5YPEEe4Bh53KMsjEfMsmMed75MuLRpH8GAb3fJAR0sEGPYVzNIrOJta62OanqTYpDU',
# 'expires_in': 3600000,
# 'token_type': 'Bearer',
# 'scope': 'androidpublisher',
# 'refresh_token': 'jGZCgAmZLEIia4I7YajCSq6dufTn2P'}



import requests
#
# def bazaar():
#     client_id = 'hrzygezwQzHmg6wzFkNxUhcV8zJYNcOlUMrtOPco'
#     client_secret = 'e6k796T0SlJx2WkVUD2hXnuOj5E5MHFK7n4GGWBnvrLUf7NpqhCgQXOa7PaX'
#     authorization_code = 'g1NuxtCRXVDkfmAFk2E0YxuALhXayg'
#     redirect_uri = 'https://api.virdaar.ir'
#
#     # ساخت URL برای دریافت Authorization Code
#     auth_url = f'https://pardakht.cafebazaar.ir/devapi/v2/auth/authorize/?response_type=code&access_type=offline&redirect_uri={redirect_uri}&client_id={client_id}'
#
#     print('Please go to this URL and authorize access:')
#     print(f'auth_url: {auth_url}')
#
#     # مقادیر دریافت شده از مرحله قبل
#     # درخواست برای دریافت توکن‌ها
#     token_url = 'https://pardakht.cafebazaar.ir/devapi/v2/auth/token/'
#     token_data = {
#         'grant_type': 'authorization_code',
#         'code': authorization_code,
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'redirect_uri': redirect_uri
#     }
#
#     response = requests.post(token_url, data=token_data)
#     tokens = response.json()
#
#     # بررسی وضعیت پاسخ و محتوای پاسخ
#     if response.status_code == 200 and 'access_token' in tokens:
#         access_token = tokens['access_token']
#         print(f'access code: {access_token}')
#         print(f'response: {response}')
#         print(f'tokens: {tokens}')
#     else:
#         print('Failed to obtain access token.')
#         print(f'response status: {response.status_code}')
#         print(f'response content: {response.text}')
#         return
#
#     package_name = 'com.monirs.virdaar'
#     api_connect = f'https://pardakht.cafebazaar.ir/devapi/v2/api/consume/{package_name}/purchases/?access_token={access_token}'
#     api_response = requests.post(api_connect)
#     api = api_response.json()
#
#     print(f'api_connect: {api_connect}')
#     print(f'api_response: {api}')
#
#     # بررسی برای دریافت refresh token
#     if 'refresh_token' in tokens:
#         refresh_token = tokens['refresh_token']
#         print(f'refresh_token: {refresh_token}')
#
#         refresh_token_data = {
#             'grant_type': 'refresh_token',
#             'client_id': client_id,
#             'client_secret': client_secret,
#             'refresh_token': refresh_token
#         }
#
#         refresh_response = requests.post(token_url, data=refresh_token_data)
#         new_tokens = refresh_response.json()
#         print(f'new_tokens: {new_tokens}')
#     else:
#         print('No refresh token available.')
#
# bazaar()


import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def bazaar():
    client_id = 'hrzygezwQzHmg6wzFkNxUhcV8zJYNcOlUMrtOPco'
    client_secret = 'e6k796T0SlJx2WkVUD2hXnuOj5E5MHFK7n4GGWBnvrLUf7NpqhCgQXOa7PaX'
    redirect_uri = 'https://api.virdaar.ir'

    # ساخت URL برای دریافت Authorization Code
    auth_url = f'https://pardakht.cafebazaar.ir/devapi/v2/auth/authorize/?response_type=code&access_type=offline&redirect_uri={redirect_uri}&client_id={client_id}'

    # استفاده از Selenium برای خودکارسازی ورود و دریافت Authorization Code
    driver = webdriver.Chrome()  # یا مرورگر دیگری مانند Firefox
    driver.get(auth_url)

    # صبر برای ورود کاربر و انجام فرآیند احراز هویت
    time.sleep(30)  # تنظیم زمان مناسب برای انجام فرآیند ورود

    # دریافت Authorization Code از URL
    current_url = driver.current_url
    driver.quit()

    # استخراج Authorization Code از URL
    if 'code=' in current_url:
        authorization_code = current_url.split('code=')[1]
    else:
        print('Failed to obtain authorization code.')
        return

    # درخواست برای دریافت توکن‌ها
    token_url = 'https://pardakht.cafebazaar.ir/devapi/v2/auth/token/'
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }

    response = requests.post(token_url, data=token_data)
    tokens = response.json()

    # بررسی وضعیت پاسخ و محتوای پاسخ
    if response.status_code == 200 and 'access_token' in tokens:
        access_token = tokens['access_token']
        print(f'access code: {access_token}')
        print(f'response: {response}')
        print(f'tokens: {tokens}')
    else:
        print('Failed to obtain access token.')
        print(f'response status: {response.status_code}')
        print(f'response content: {response.text}')
        return

    package_name = 'com.monirs.virdaar'
    api_connect = f'https://pardakht.cafebazaar.ir/devapi/v2/api/consume/{package_name}/purchases/?access_token={access_token}'
    api_response = requests.post(api_connect)
    api = api_response.json()

    print(f'api_connect: {api_connect}')
    print(f'api_response: {api}')

    # بررسی برای دریافت refresh token
    # if 'refresh_token' in tokens:
    #     refresh_token = tokens['refresh_token']
    #     print(f'refresh_token: {refresh_token}')
    #
    #     refresh_token_data = {
    #         'grant_type': 'refresh_token',
    #         'client_id': client_id,
    #         'client_secret': client_secret,
    #         'refresh_token': refresh_token
    #     }
    #
    #     refresh_response = requests.post(token_url, data=refresh_token_data)
    #     new_tokens = refresh_response.json()
    #     print(f'new_tokens: {new_tokens}')
    # else:
    #     print('No refresh token available.')

    product_id='VIRDAAR-TEST'
    purchase_token='24184010292103'
    package_name = 'com.monirs.virdaar'
    ur = f'validate/{package_name}/inapp/{product_id}/purchases/{purchase_token}/'
    # درخواست به API مورد نظر
    api_url = f'https://pardakht.cafebazaar.ir/devapi/v2/api/{ur}'
    headers = {
        'Authorization':access_token
    }

    api_response = requests.get(api_url, headers=headers)
    api_result = api_response.json()

    print(f'api_result; {api_result}')
    # except:
# v=bazaar()
# print(f'v :{v}')

i='XpD7lRjoetV54Fuej0tUcLhOmlMjzR'
print(len(f'i:{i}'))
