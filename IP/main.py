from requests import get, post, put, ConnectionError
from json import dumps, loads
from time import sleep, time
from uuid import uuid4
from threading import Thread
from re import findall
from os import rename, remove
# from user_agent import generate_user_agent
from user_agents import parse

acc_num = 0
head_clickro = {
    "sec-ch-ua": "'Not)A;Brand';v='24', 'Chromium';v='116'",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "User-Agent": parse("android"),
    "sec-ch-ua-platform": "Android",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, utf-8",
    "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
}

def print_low(string):
    for char in string:
        print(char, end='', flush=True)
        sleep(0.0)

def write_to_file(filename, text, mode="a+"):
    with open(filename, mode, encoding="utf8") as f:
        f.write(text)

def read_from_file(filename):
    with open(filename, "r", encoding="utf8") as f:
        return f.read()

def filter_and_rename_file(filename, used):
    with open(filename, 'r', encoding="utf8") as file:
        lines = file.readlines()
    new_lines = [line for line in lines if line.strip() not in used]
    temp_filename = f"new-{filename}"
    with open(temp_filename, 'w', encoding="utf8") as new_file:
        new_file.writelines(new_lines)
    remove(filename)
    rename(temp_filename, filename)
    
def split_and_write_to_file(filename, item_list, num, failed):
    x = [f"UnUsed => {i}\n" for i in item_list[num:]] + \
        [f"Used => {i}\n" for i in item_list[:num] if i not in failed] + \
        [f"Failed => {i}\n" for i in failed]

    temp_filename = f"new-{filename}"
    with open(temp_filename, 'w', encoding="utf8") as new_file:
        new_file.writelines(x)
    remove(filename)
    rename(temp_filename, filename)

##############
def create_address(token,uid):
    url = f"https://api.snapp.express/mobile/v4/user/address/create?client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&clientVersion=ba494030&optionalVersion=5.6.6&UDID={uid}"
    headers = {
        "Host": "api.snapp.express","Content-Length": "510","Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',"Accept": "application/json, text/plain, */*","Content-Type": "application/x-www-form-urlencoded","Sec-Ch-Ua-Mobile": "?1","Authorization": token,"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S911U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36","Sec-Ch-Ua-Platform": "Android","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, utf-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = {
        "cityId": "1","phone": "09378540745","label": "","address": "، تهران، جردن - پارک ملت، بلوار نلسون مندلا، مهرداد بعد از سید رضا سعیدی","address_extra": "پلاک 4","latitude": "35.773643","longitude": "51.418311","city_id": "1","local": ""
    }

    response = post(url, headers=headers, data=data).json()
    return response.get("data")["address"]["id"]


def get_address(token,uid):
    url = f"https://api.snapp.express/mobile/v1/user/user-addresses-subscription?vendorCode=po9qzk&lastLatitude=35.773&lastLongitude=51.419&client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&clientVersion=ba494030&optionalVersion=5.6.6&UDID={uid}"
    headers = {
        "Host": "api.snapp.express","Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',"Accept": "application/json, text/plain, */*","Sec-Ch-Ua-Mobile": "?1","Authorization": token,"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S911U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36","Sec-Ch-Ua-Platform": "Android","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, utf-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    response = get(url, headers=headers).json()
    addresses = response['data']['addresses']
    if len(addresses) != 0:
        return addresses[0]['id']
    else:
        return create_address(token,uid)
	
def add_to_cart(token,cart_id,uid):
    products = [4076711]#4076720
#4433771
    url = f"https://api.snapp.express/cart/v1/{cart_id}?variable={cart_id}&client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&clientVersion=ba494030&optionalVersion=5.6.6&UDID={uid}"
    headers = {
        "Host": "api.snapp.express","Content-Length": "147","Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',"Accept": "application/json, text/plain, */*","Content-Type": "application/json","Sec-Ch-Ua-Mobile": "?1","Authorization": token,"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S911U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36","Sec-Ch-Ua-Platform": "Android","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, uft-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    kossher = list()
    for i in products:
        data = {
            "actions": {
                "products": [{"id": str(i), "type": "INCREMENT"}]
            },
            "platform": "PWA",
            "UDID": uid,
            "app_version": "5.6.6"
        }
        response = put(url, headers=headers, json=data)
        kossher.append(str(response.status_code))
    return kossher

def create_cart(token,uid, address):
    url = f"https://api.snapp.express/cart/v1?client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&clientVersion=ba494030&optionalVersion=5.6.6&UDID={uid}"
    headers = {
    "Host": "api.snapp.express","Content-Length": "224","Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',"Accept": "application/json, text/plain, */*","Content-Type": "application/json","Sec-Ch-Ua-Mobile": "?1","Authorization": token,"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S911U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36","Sec-Ch-Ua-Platform": "Android","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, utf-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = {
        "actions": {
            "vendor": {"code": "po9qzk"},
            "source": {"name": "PWA"},
            "address": {"id": int(address)},
            "products": [{"id": "4077096", "type": "INCREMENT"}]
        },"platform": "PWA","UDID": str(uid),
        "app_version": "5.6.6"
    }
    response = post(url, headers=headers, json=data).json()
    kossher = add_to_cart(token,str(response["cart"]["id"]),str(uid))
    # [0] : cart id , [1] : cart maximum price
    return [response["cart"]["id"],response["cart"]["prices"]["total"]]

	########
def get_token(uuid):
    headers = {"Host": "api.snapp.express","content-length": "209","sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',"accept": "application/json, text/plain, */*","content-type": "application/json","sec-ch-ua-mobile": "?1","user-agent": parse("android"),"sec-ch-ua-platform": "Android","origin": "https://snapp.express","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://snapp.express/","accept-encoding": "gzip, deflate, uft-8","accept-language": "fa-IR,fa;q=0.9"}
    payload = {"data": {"grant_type": "password","device_uid": str(uuid),"time": int(time()),"client_id": "snappfood_pwa","scope": "mobile_v2 mobile_v1 webview","client_secret": "snappfood_pwa_secret"}}
    response = post(url="https://api.snapp.express/oauth2/default/token", headers=headers, data=dumps(payload)).json()
    return f"Bearer {response['data']['access_token']}"

    
def snapp_sso(uuid,token,auth):
    url = "https://api.snapp.express/mobile/v2/user/snapp-sso"
    headers = {"Host": "api.snapp.express","sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',"accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?1","authorization": auth,"user-agent": parse("android"),"sec-ch-ua-platform": "Android","origin": "https://snapp.express","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://snapp.express/","accept-encoding": "gzip, deflate, utf-8","accept-language": "fa-IR,fa;q=0.9"}
    params = {"token": token,"sso_channel": "food","client": "MOBILE_WEB","optionalClient": "MOBILE_WEB","deviceType": "MOBILE_WEB","appVersion": "5.6.6","clientVersion": "33db1c33","optionalVersion": "5.6.6","UDID": str(uuid)}
    responsee = get(url, headers=headers, params=params).json()
    return responsee['data']['oauth2_token']['access_token']

###############

def get_basket(token):
    headers = {"accept": "application/json, text/plain, */*","content-type": "application/json","accept-language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7","accept-encoding": "gzip, deflate, utf-8","authorization": token,"referer": "https://snapp.express/","origin":"https://snapp.express","sec-ch-ua": "'Chromium';v='116', 'Not)A;Brand';v='24', 'Google Chrome';v='116'","sec-ch-ua-mobile": "?1","sec-ch-ua-platform": "Android","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-site","User-Agent": parse("android")}
    try:
        uid = uuid4()
        address = get_address(token,uid)
        cart = create_cart(token,uid, address)
        print(f"id => {cart[0]} / \33[93mMax : {cart[1]}\033[0m")
        return [token, cart[0]]
    except:
        pass

def retoken(refresh_token):
    headers = {"Host": "api.snapp.express","Content-Length": "1119","sec-ch-ua": "'Not)A;Brand';v='24', 'Chromium';v='116'","Accept": "application/json, text/plain, */*","Content-Type": "application/json","sec-ch-ua-mobile": "?1","User-Agent": parse("android"),"sec-ch-ua-platform": "Android","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, utf-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"}
    data = {"data": {"grant_type": "refresh_token","device_uid": str(uuid4()),"time": int(time()),"refresh_token": refresh_token,"client_id": "snappfood_pwa","scope": "mobile_v2 mobile_v1 webview","client_secret": "snappfood_pwa_secret"}}
    response = post("https://api.snapp.express/oauth2/default/token", headers=headers, json=data).json()
    
    if response['status'] == True:
        return response['data']['access_token']
    else:
        print(response['error']['message'])
        return False
    
def get_auth(url_list):
    global acc_num
    global need_retoken
    global Failed
    url = url_list[acc_num]
    if 'exp-clickro.info' in url or 'hirmanro.com' in url:
        response = get(url).text.split('''class="textbox"
            value="''')[1].split('''"
            onclick="copyText()"''')[0].replace('&#34;','"')
        jwt = loads(response)['JWT']
        if need_retoken and 'exp-clickro.info' not in url:
            token_again = retoken(str(loads(jwt)['refresh_token']))
            if token_again != False:
                token = 'Bearer ' + str(token_again)
            else:
                write_to_file(filename="invalids.txt", text=f"{url}\n")
                Failed.append(url)
                acc_num += 1
                return get_auth(url_list)
        else:
            token = 'Bearer ' + str(loads(jwt)['access_token'])
    if 'exp-clickro.top' in url:
        main_uuid = uuid4()
        clickro_token_1 = get(url,headers=head_clickro)
        if "exp.clickro.ir" in clickro_token_1.headers['refresh']:
            clickro_token = get(url,headers=head_clickro, cookies=clickro_token_1.cookies).headers['refresh'].split("url=")[1].split("token=")[1].split("&")[0]
        else:
            clickro_token = clickro_token_1.headers['refresh'].split("url=")[1].split("token=")[1].split("&")[0]
        token = 'Bearer ' + snapp_sso(main_uuid,clickro_token,get_token(main_uuid))
    else:
        response = get(url.replace('/raw', '')).text
        # 
    basket = get_basket(token)
    if basket is not None:
        #0 = author & 1 = basket_id
        return [basket[0],basket[1]]
    else:
        Failed.append(url)
        acc_num += 1
        return get_auth(url_list)
        
def send_request(token, user_id_list,uuid=uuid4()):
    global acc_num
    global author
    global user_id
    global used
    url = f"https://api.snapp.express/cart/v1/{user_id}?variable={user_id}&client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&clientVersion=ba494030&optionalVersion=5.6.6&UDID={uuid}"
    data = {"actions":{"voucher":{"code":token}},"platform":"PWA","UDID":str(uuid),"app_version":"5.6.6"}
    headers = {"Host": "api.snapp.express","Content-Length": "70","Sec-Ch-Ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"","Accept": "application/json, text/plain, */*","Content-Type": "application/json","Sec-Ch-Ua-Mobile": "?1","Authorization":author,"User-Agent": parse("android"),"Sec-Ch-Ua-Platform": "\"Android\"","Origin": "https://snapp.express","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://snapp.express/","Accept-Encoding": "gzip, deflate, utf-8","Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"}
    try:
        response = put(url=url, json=data, headers=headers, timeout=8).json()
        if len(response) != 1:
            if response.get("success", False):
                # for item in response['data']['basket']['prices']:
                #     if item['alias'] == 'VOUCHER_DISCOUNT_PRICE':
                #         value = item['value']
                #     else:
                value = "OK-SHOD"
                print(f"\33[92m{token}{value}")
                write_to_file(filename="Goods.txt", text=f"{token}\n")
                used.append(token)
            else:
                resource_exhausted_errors = response.get('resource_exhausted_error', {}).get('errors', [])
                validation_errors = response.get('validation_error', {}).get('errors', [])
                not_found_error = response.get('not_found_error', {}).get('errors', [])
                auth_error = response.get('auth_error', {}).get('errors', [])
                canceled_error = response.get('canceled_error', {}).get('errors', [])
                error_messages = []
                error_messages.extend([str(error['code']) for error in resource_exhausted_errors if error.get('code')])
                error_messages.extend([str(error['code']) for error in validation_errors if error.get('code')])
                error_messages.extend([str(error['code']) for error in not_found_error if error.get('code')])
                error_messages.extend([str(error['code']) for error in auth_error if error.get('code')])
                error_messages.extend([str(error['code']) for error in canceled_error if error.get('code')])
                
                if 'VOUCHER_FOR_NEW_USER' in error_messages:
                    value = "NEW-USER"
                    print(f"\33[92m{token}{value}\033")
                    write_to_file(filename="Goods.txt", text=f"{token}\n")
                    used.append(token)
                    
                elif 'VOUCHER_MIN_ORDER_VALUE_VIOLATION' in error_messages:
                    value="VALID"
                    print(f"\33[92m{token}{value}\033")
                    write_to_file(filename="Goods.txt", text=f"{token}\n")
                    used.append(token)
                    
                elif 'VOUCHER_NOT_FOUND' in error_messages:
                    print(f"\033[1;31m{token}\033[0m")
                    used.append(token)
                    
                elif 'NOT_DELIVERIABLE' in error_messages :
                	value='delivery'
                	print (f'\033[1;31m{token}\033[0m')
                	write_to_file(filename='Goods.txt' , text=f"{token}\n")
                elif 'VOUCHER_USED_BEFORE' in error_messages:
                    print(f"\33[93m{token}\033[0m")
                    used.append(token)
                    
                elif 'RATE_LIMIT_EXCEEDED' in error_messages:
                    print(f"\33[96mLIMITED\033[0m")
                    acc_num += 1
                    get_info = get_auth(user_id_list)
                    author = get_info[0]
                    user_id = get_info[1]
                    
                elif 'VOUCHER_NOT_APPLICABLE' in error_messages:
                    value = "APPLICABLE"
                    print(f"\33[92m{token}{value}\033")
                    write_to_file(filename="Goods.txt", text=f"{token}\n")
                    used.append(token)
                    
                elif 'VOUCHER_VENDOR_NOT_ALLOWED' in error_messages:
                    value = "SHOP"
                    print(f"\33[92m{token}{value}\033")
                    write_to_file(filename="Goods.txt", text=f"{token}\n")
                
                elif 'VOUCHER_NOT_FOUND' in error_messages:
                    print(f"\033[1;31m{token}(\033[0m")
                    used.append(token)
        else:
            print("The Basket Has Been Expired or Closed")
    except:
        pass

if __name__ == "__main__":
    try:
        print_low(f"""\33[94m  CHECKER EXPRESS \n
           \033\n\033[0m\n{'='*34}\n""")

        user_id_list = findall("https?://\S+",read_from_file("user-id.txt"))
        used = []
        Failed = []
        filename = input("Enter file name: ")
        need_retoken = True if input("Your Khat's Needs Getting New Token ? (Y/N) :").lower() == "y" else False
        count = 1
        for item in read_from_file(filename).split("\n"):
            if (count % 30 == 0) or acc_num == 0:
                try:
                    if acc_num == 0:
                        acc_num += 1
                    count = 1
                    get_info = get_auth(user_id_list)
                    author = get_info[0]
                    user_id = get_info[1]
                except ConnectionError:
                    print("")
                  
                except Exception as e:
                    print(e,"")
                  
            else:
                send_request(item, user_id_list)
                count += 1

    except Exception as e:
        print("Error:", e)
