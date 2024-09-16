from Snapp.models import *
#
# data=[{"transaction_code": 54, "customer_code": 12, "price": 3422222, "date": "2024-01-21 11:38:10.053216", "bank": "te", "tracking_code": 505}, {"transaction_code": 3, "customer_code": 12, "price": 300000, "date": "2024-01-21 11:47:23.008398", "bank": "ted", "tracking_code": 669}, {"transaction_code": 2, "customer_code": 12, "price": 5670000, "date": "2024-01-21 11:49:51.407536", "bank": "sepah", "tracking_code": 191}, {"transaction_code": 2, "customer_code": 12, "price": 23455, "date": "2024-01-22 13:27:12.138075", "bank": "2323", "tracking_code": 204}, {"transaction_code": 12, "customer_code": 12, "price": 1000000, "date": "2024-01-22 15:16:05.803789", "bank": "tejarat", "tracking_code": 396}, {"transaction_code": 10, "customer_code": 12, "price": 10000000, "date": "2024-01-23 13:20:35.010458", "bank": "tej", "tracking_code": 681}, {"transaction_code": 12, "customer_code": 12, "price": 3000000, "date": "2024-01-23 15:08:00.040226", "bank": "tej", "tracking_code": 103}, {"transaction_code": 42, "customer_code": 12, "price": 120000, "date": "2024-01-24 09:00:39.164409", "bank": "meli", "tracking_code": 214}, {"transaction_code": 32, "customer_code": 12, "price": 120000, "date": "2024-01-24 09:07:40.186910", "bank": "tej", "tracking_code": 443}, {"transaction_code": 50, "customer_code": 12, "price": 300, "date": "2024-01-24 09:09:54.166675", "bank": "mehr", "tracking_code": 186}, {"transaction_code": 1, "customer_code": 12, "price": 1, "date": "2024-01-24 09:10:57.260976", "bank": "r", "tracking_code": 431}, {"transaction_code": 22, "customer_code": 12, "price": 22, "date": "2024-01-24 09:13:14.680665", "bank": "w", "tracking_code": 310}, {"transaction_code": 123, "customer_code": 12, "price": 123, "date": "2024-01-24 09:14:47.866590", "bank": "1", "tracking_code": 938}, {"transaction_code": 1, "customer_code": 12, "price": 12, "date": "2024-01-24 13:27:09.368483", "bank": "we", "tracking_code": 765}, {"transaction_code": 1, "customer_code": 10, "price": 1, "date": "2024-01-24 14:24:25.216857", "bank": "2", "tracking_code": 229}, {"transaction_code": 34, "customer_code": "djs", "price": 12341, "date": "2024-01-24 15:03:50.925821", "bank": "qe", "tracking_code": 939}, {"transaction_code": 12, "name_customer": "djs", "price": 4323, "date": "2024-01-24 15:39:22.686604", "bank": "12", "tracking_code": 821}, {"transaction_code": 13, "name_customer": "djs", "price": 123000, "date": "2024-01-31 10:37:07.515709", "bank": "tip", "tracking_code": 729}, {"transaction_code": 43, "name_customer": "djs", "price": 3000000, "date": "2024-01-31 10:37:52.248661", "bank": "tej", "tracking_code": 565}, {"transaction_code": 1, "name_customer": "djs", "price": 2000000, "date": "2024-01-31 10:43:46.425932", "bank": "tej", "tracking_code": 216}, {"transaction_code": 43, "name_customer": "djs", "price": 500000, "date": "2024-01-31 10:50:05.132646", "bank": "tej", "tracking_code": 254}, {"transaction_code": 12, "name_customer": "djs", "price": 500000, "date": "2024-01-31 10:51:51.664786", "bank": "tej", "tracking_code": 459}, {"transaction_code": 54, "name_customer": "djs", "price": 3000000, "date": "2024-01-31 10:53:17.749850", "bank": "tej", "tracking_code": 812}, {"transaction_code": 32, "name_customer": "djs", "price": 3000000, "date": "2024-01-31 11:07:20.384502", "bank": "tej", "tracking_code": 213}, {"transaction_code": 43, "name_customer": "djs", "price": 5000000, "date": "2024-01-31 11:08:50.885745", "bank": "tej", "tracking_code": 127}, {"transaction_code": 43, "name_customer": "djs", "price": 4000000, "date": "2024-01-31 11:10:42.082186", "bank": "tej", "tracking_code": 299}, {"transaction_code": 12, "name_customer": "djs", "price": 3000000, "date": "2024-01-31 11:14:51.583312", "bank": "tej", "tracking_code": 672}]
# for d in data:
#     new_obj = Transaction(
        # transaction_code = d['transaction_code'],
        # customer_code=d['customer_code'],
        # price = d['price'],
        # date=d['date'],
        # bank = d['bank'],
        # traking_code = d['tracking_code']
    # )
    # new_obj.save()


# data=[{"customer_code": 10, "manager_code": 10, "name": "dksd", "familly": "dksd", "addres": "sdkd", "phone_number": 1234}, {"customer_code": 11, "manager_code": 1, "name": "djs", "familly": "djsj", "addres": "sdj", "phone_number": 914}, {"customer_code": 12, "manager_code": 2, "name": "jak", "familly": "jaki", "addres": "pachenar", "phone_number": 918}]
# for d in data:
#     new_obj =Customer(
#     customer_code = d['customer_code'],
#     name = d['name'],
#     familly = d['familly'],
#     addres = d['addres'],
#     phone_number = d['phone_number'],
    # location_driv = d['location_driv']
    #     )
    # new_obj.save()

# data=[{"code": 6, "name": "jsdsda", "familly": "sdjsdk", "addres": "sdjsd skd ", "phone_number": 912, "user_name": "fsdjsd", "password": 123}, {"code": 4, "name": "hasan", "familly": "hasenvand", "addres": "dareh garm ", "phone_number": 913, "user_name": "fsdjsd", "password": 321}, {"code": 3, "name": "nima", "familly": "namiie", "addres": "poshteh", "phone_number": 918, "user_name": "nima74", "password": 231}]
# for d in data:
#     new_obj =SnappManager(
#     code =  d['code'],
#     name = d['name'],
#     familly =  d['familly'],
#     addres =  d['addres'],
#     phone_number =  d['phone_number'],
#     user_name =  d['user_name'],
#     password =  d['password'],
#         )
#     new_obj.save()

# data=[{"manager_code": 4, "driver_code": 5, "name": "ali", "familly": "5", "phone_number": 5, "address": "5", "national_code": 5, "model_car": "5", "color": "5", "plaque_car": 5, "location_driv": {"lenght": 5, "width": 5}}, {"manager_code": 4, "driver_code": 1, "name": "ahmad", "familly": "1", "phone_number": 1, "address": "1", "national_code": 1, "model_car": "1", "color": "1", "plaque_car": 1, "location_driv": {"lenght": 111, "width": 100}}, {"manager_code": 4, "driver_code": 3, "name": "32", "familly": "3", "phone_number": 2, "address": "2", "national_code": 2, "model_car": "2", "color": "2", "plaque_car": 2, "location_driv": {"lenght": 1, "width": 2}}, {"manager_code": 4, "driver_code": 4, "name": "hamed", "familly": "abdoli", "phone_number": 917, "address": "kurosh", "national_code": 4060, "model_car": "1360", "color": "black", "plaque_car": 42, "location_driv": {"lenght": 23, "width": 23}}]
# for d in data:
#     new_obj =Driver(
#     manager_code =d['manager_code'],
#     driver_code = d['driver_code'],
#     name = d['name'],
#     familly = d['familly'],
#     phone_number = d['phone_number'],
#     address = d['address'],
#     national_code = d['national_code'],
#     model_car = d['model_car'],
#     color = d['color'],
#     plaque_car = d['plaque_car'],
#     location_driv = d['location_driv'],
#         )
#     new_obj.save()



# for d in data:
#     new_obj =Driver(
#     manager_code =d['manager_code'],
#     driver_code = d['driver_code'],
#     name = d['name'],
#     familly = d['familly'],
#     phone_number = d['phone_number'],
#     address = d['address'],
#     national_code = d['national_code'],
#     model_car = d['model_car'],
#     color = d['color'],
#     plaque_car = d['plaque_car'],
#     location_driv = d['location_driv'],
#         )
#     new_obj.save()