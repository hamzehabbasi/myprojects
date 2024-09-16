# import requests

import requests
import json


# client_id ='4yaLBrmIQQmqqfmm3kE0vRqanOrhWD4oPSd9MTXz'
# client_secret ='9trgtGtSKBMVKZKCSZFopk7vnQXCbpFAhfq3JwJgUeldY1dU3aDMGxXHyTyd'
# code='cjCvCoX6OQ3EzHk7n517klNzCTFakB'
# redirect_uri='https://api.virdaar.ir'
packageName='com.monirs.virdaar'
offset=1
Limit=10
def get_access_token():
        url = f'https://developer.myket.ir/api/partners/applications/com.monirs.virdaar/release-bundle'
        headers = {
            'X-Access-Token':'b15d5bda-6d28-4160-b947-9fb1d3b14345'
        }
        response = requests.get(url, headers=headers)
        print(f'response={response.content}')
        return response


access_token = get_access_token()
print(access_token)














# # اطلاعات ورود به API
# client_id = 'YOUR_CLIENT_ID'
# client_secret = 'YOUR_CLIENT_SECRET'
#
# # احراز هویت و دریافت توکن
# def get_access_token(client_id, client_secret):
#     url = 'https://auth.cafebazaar.ir/oauth/token'
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#     data = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret,
#     }
#     response = requests.post(url, headers=headers, data=data)
#     return response.json()['access_token']
#
# access_token = get_access_token(client_id, client_secret)
#
# # فراخوانی یک endpoint از API
# def call_api(endpoint, access_token):
#     url = f'https://pardakht.cafebazaar.ir/devapi/v2/{endpoint}'
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }
#     response = requests.get(url, headers=headers)
#     return response.json()
#
# # مثال: دریافت اطلاعات یک برنامه
# app_info = call_api('applications/package_name', access_token)
# print(app_info)
