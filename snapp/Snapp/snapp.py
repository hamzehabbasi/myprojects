from Snapp.models import *
from Snapp.snapp_module import *
# import json
import math
import random
import datetime

class Snapp():

    # JSON_MANAGER
    snapp_ma=SnappManager.objects.all()
    snapp_ma= [x.api() for x in snapp_ma]

    # DRIVER
    drivers=Driver.objects.all()
    drivers= [x.api() for x in drivers]

    # CUSTOMER
    snapp_customer=Customer.objects.all()
    snapp_customer= [x.api() for x in snapp_customer]

    # SERVISE_CHARGE
    servise_charge=Service_charge.objects.all()
    servise_charge= [x.api() for x in servise_charge]

    # TRANSACATION
    transaction=Transaction.objects.all()
    transaction= [x.api() for x in transaction]

    # TRANSACATION
    take_servise=Servise.objects.all()
    take_servise= [x.api() for x in take_servise]

    # _COMMENTS_CUSTOMER
    say_comment=Register_a_comment.objects.all()
    say_comment= [x.api() for x in say_comment]

    # WALLET_CUSTOMER
    wallet_customer=Customer.objects.all()
    wallet_customer= [x.api() for x in wallet_customer]
    for i in wallet_customer:
        wallet_customer=i['wallet_customer']

    # SEND_T0_DRIVER
    suggestion_driver=SuggesDriver.objects.all()
    suggestion_driver=[x.api() for x in suggestion_driver]

    # PRICE_SERVICE_DRIVER
    price_service_driver=SuggesDriver.objects.all()
    price_service_driver=[x.api() for x in price_service_driver]
    for i in price_service_driver:
        price_service_driver = i['price_trip']

    # WALLET_DRIVER
    wallet_driver=Driver.objects.all()
    wallet_driver= [x.api() for x in wallet_driver]
    for i in wallet_driver:
        wallet_driver=i['wallet_driver']

    while True:
        i = input('you 1.Snapp_manager or 2.Customer  or 3.driver?')
        # INFORM_SNAPP_MANAGER
        if i == '1':
            passwo = int(input('enter your password:'))
            for s_m in snapp_ma:
                password = s_m['password']
                if passwo == password:
                    print('you joined')
                    while True:
                        work_manager = ['register new snapp_manager','register_driver','service_pay']
                        work_manager = make_list(work_manager)
                        print()
                        print(f'the snapp_manager can do:\n{work_manager}')
                        print()
                        prefer = input('which one wnat to do ?(0 for exit)')
                        if prefer == '1':

                            code = int(input('enter a code:'))
                            name = input('enter the name:')
                            familly = input('enter the familly')
                            addres = input('enter the addres:')
                            phone_number = int(input('enter phone_number:'))
                            user_name = input('enter user_name')
                            password = int(input('password:'))
                            # SNAPP_MANAGER
                            snapp_manager = SnappManager(
                                code=code,
                                name = name,
                                familly =familly,
                                addres = addres,
                                phone_number = phone_number,
                                user_name = user_name,
                                password = password,
                            )
                            snapp_ma.append(snapp_manager)
                            snapp_manager.save()

                        # DRIVERS
                        elif prefer == '2':
                            print( )
                            location_driv = Location(
                                lenght=int(input('enter the lenght:')),
                                width=int(input('enter the width:'))
                            )
                            location_driv=location_driv.api()

                            lenght=[]
                            lenght.append(location_driv['lenght'])
                            width=[]
                            width.append(location_driv['width'])
                            location_driv=math.dist(lenght,width)

                            driver_code = int(input('enter driver_code:'))
                            name = input('enter the name:')
                            familly = input('enter the familly:')
                            phone_number = int(input('enter phone_number:'))
                            address = input('enter the address:')
                            national_code = int(input('enter nationam_code:'))
                            model_car = input('enter model_car:')
                            color = input('enter model_car:')
                            plaque_car = int(input('enter plaque_car:'))
                            wallet_driver = int(input('charge the wallet:'))

                            snapp_driver = Driver(
                                manager_code=passwo,
                                driver_code=driver_code,
                                name = name,
                                familly = familly,
                                phone_number = phone_number,
                                address = address,
                                national_code = national_code,
                                model_car = model_car,
                                color = color,
                                plaque_car = plaque_car,
                                location_driv = location_driv,
                                wallet_driver = wallet_driver,
                                )
                            # drivers.append(snapp_driver)
                            snapp_driver.save()

                            show_drivers_list=input('do you want to see drivers list?(yes/no)\n\n')
                            if show_drivers_list== 'yes':
                                driv=Driver.objects.all()
                                drivers_list=[x.api() for x in driv]
                                print(f'the list of drivers:\n{list_kardan(drivers_list)}')

                        # SERVICE_PAY
                        elif prefer == '3':
                            o = input('you want to pay price service driver[yes or no]?')
                            if o == 'yes':
                                print('you joined')
                                try:
                                    # WALLET_DRIVER
                                    price_service_driv = price_service_driver
                                    delete=SuggesDriver.objects.all()
                                    delete.delete()

                                    for m in snapp_ma:
                                        m = m['code']
                                        for d in drivers:
                                            code_driv = d['driver_code']
                                            servise = Service_charge(
                                                manager_code = m,
                                                driver_co = code_driv,
                                                service_charg_code = random.randint(200,400),
                                                price = price_service_driver,
                                                tracking_code = random.randint(200,400),
                                                  )
                                            servise_charge.append(servise)
                                            servise.save()
                                            servise_charge=[x.api() for x in servise_charge]
                                    print(f'list of servise_charge:{list_kardan(servise_charge)}')
                                except:
                                    print('you dont have a service ')

                        else:
                            break
                else:
                    print('your password is not correct.')

        # CUSTOMER
        elif i == '2':
            while True:
                exist_customer = ['don,t have an account?', 'have an account?']
                exist_customer = make_list(exist_customer)
                print()
                print(f'the customer can do:\n{exist_customer}')
                print()
                prefer_c = input('which one wnat to do?(0 for exit)')

                # DON,T HAVE AN ACCOUNT
                if prefer_c == '1':
                    customer_code = int(input('enter customer_code:'))
                    name = input('enter a name:')
                    familly = input('enter a familly:')
                    addres = input('enter a address:')
                    phone_number = int(input('enter phone_number:'))
                    location_driv = random.randint(100, 1000)
                    wallet_customer = int(input('enter wallet_customer:'))

                    customer = Customer(
                        customer_code=customer_code,
                        name = name,
                        familly = familly,
                        addres = addres,
                        phone_number = phone_number,
                        location_driv = location_driv,
                        wallet_customer = wallet_customer,
                    )
                    snapp_customer.append(customer)
                    customer.save()

                    show_customer_list=input('do you want to see customer list?(yes/no)\n\n')
                    if show_customer_list == 'yes':
                        cu=Customer.objects.all()
                        customer_list=[x.api() for x in cu]
                        print(f'the list of drivers:\n{list_kardan(customer_list)}')
                # HAVE AN ACCOUNT
                elif prefer_c == '2':
                    code = int(input('enter your customer_code:'))
                    for c in snapp_customer:
                        c1 = c['customer_code']
                        if code == c1:
                            while True:
                                print(f'you joined')
                                work_customer = ['transation', 'take_servise', 'opinion']
                                work_customer = make_list(work_customer)
                                print(f'\nthe customer can do:\n\n{work_customer}')
                                work = input('enter a option or 0 for exit:')
                                c2 = c['name']
                                wallet_cus=c['wallet_customer']

                                # TRANSACTION
                                if work == '1':
                                    transaction_code = int(input('enter the transaction_code:'))
                                    price = int(input('enter the peice:'))
                                    bank = input('enter the bank:')

                                    transac = Transaction(
                                        customer_name=c2,
                                        transaction_code = transaction_code,
                                        price = price,
                                        bank = bank,
                                        traking_code = random.randint(100,1000)
                                    )
                                    transaction.append(transac)
                                    transac.save()

                                    show_transaction_list = input('do you want to see transaction list?(yes/no)\n\n')
                                    if show_transaction_list == 'yes':
                                        cu = Transaction.objects.all()
                                        transaction_list = [x.api() for x in cu]
                                        print(f'list of transaction:\n\n{list_kardan(transaction_list)}')

                                # TAKE_SERVICE
                                elif work == '2':
                                    print('\nstart_location:\n')
                                    lenght=int(input('enter lenght:'))
                                    width=int(input('enter width:'))
                                    start_location = Location(
                                        lenght=lenght,
                                        width=width
                                    )
                                    start_location.save()
                                    start_location=start_location.api()

                                    lenght2 = []
                                    l=start_location['lenght']
                                    lenght2.append(l)
                                    width2 = []
                                    width2.append(start_location['width'])

                                    start_l = math.dist(lenght2, width2)
                                    start_locati=[]
                                    start_locati.append(start_l)

                                    print('end location:')
                                    lenght=int(input('enter lenght:'))
                                    width=int(input('enter width:'))
                                    end_location = Location(
                                        lenght=lenght,
                                        width=width
                                    )
                                    end_location.save()

                                    end_location=end_location.api()

                                    lenght3 = []
                                    l=end_location['lenght']
                                    lenght3.append(l)

                                    width3 = []
                                    width3.append(end_location['width'])

                                    end_l = math.dist(lenght3, width3)

                                    price_travel = []

                                    start_loc = sorted(start_location.values())
                                    end_loca = sorted(end_location.values())

                                    # FIND NEAREST CAR
                                    pla=0
                                    v=''
                                    nearest_car=0
                                    name_dri_space = []
                                    list_spaces = []
                                    for l_d in drivers:
                                        loca_d=[]
                                        lo = l_d['location_driv']
                                        loca_d.append(lo)
                                        print(f'driver location:{loca_d}')
                                        f = math.dist(start_locati, loca_d)
                                        v = l_d['name']
                                        fs = {v: f}
                                        name_dri_space.append(fs)
                                        list_spaces.append(f)

                                        nearest_car = min(list_spaces)
                                        pla = l_d['plaque_car']

                                    # price_travel
                                    space_start_end = math.dist(start_loc, end_loca)
                                    price_travel.append(space_start_end * 1000)
                                    for i in price_travel:
                                        price_travel=i
                                    # SHOW_NAME_DRIVER
                                    take_s=0
                                    for i in name_dri_space:
                                        for x in i:
                                            if nearest_car in i.values():
                                                print()
                                                print( f'infomation_service:space between start ane end:{space_start_end}km \nthe price:{price_travel} \n driver:{i.keys()},')

                                                # JSON_SERVISE
                                                take_s = Servise(
                                                    drive_nam=v,
                                                    plaq_car = pla,
                                                    customer_name = c2,
                                                    location_start = start_l,
                                                    location_end = end_l,
                                                    price_travel = price_travel
                                                    )
                                                take_s.save()
                                                take_s=take_s.api()

                                    # CHARGE
                                    if price_travel > wallet_cus:
                                        print('your money is lower than price_travel.')
                                        charge = input('you want to charge(1 = yes, 0 = no)?')
                                        if charge == '1':
                                            transaction_code = int(input('enter the transaction_code:'))
                                            price = int(input('enter the peice:'))
                                            bank = input('enter the bank:')
                                            transac = Transaction(
                                                customer_name=c2,
                                                transaction_code=transaction_code,
                                                price=price,
                                                bank=bank,
                                                traking_code=random.randint(100, 1000)
                                            )
                                            transaction.append(transac)
                                            transac.save()
                                            print(f'your account charged')

                                            transac=transac.api()

                                            # WALLET_CUSTOMER
                                            wallet_cust = transac['price'] + wallet_cus
                                            print(f'customer customer: {wallet_cust}')

                                            # the for,for exist the price from the list
                                            remaining_money_customer = wallet_cust - price_travel

                                            snapp_custome=Customer.objects.all()
                                            for j in snapp_custome:
                                                if j.customer_code == c1:
                                                    j.wallet_customer = remaining_money_customer
                                                    j.save()
                                            print(f'remaining money customer: {remaining_money_customer}')

                                        elif charge == '0':
                                            print('your request canceled')
                                            take_s.delete()
                                            break
                                    else:

                                        remaining_money_customer = wallet_cus - price_travel

                                        snapp_custome = Customer.objects.all()
                                        for j in snapp_custome:
                                            if j.customer_code == c1:
                                                j.wallet_customer = remaining_money_customer
                                                j.save()
                                        print(f'remaining money customer: {remaining_money_customer}')
                                    # SEND THE REQUEST TO DRIVER:
                                    for i in name_dri_space:
                                        for x in i:
                                            if nearest_car in i.values():
                                                print(f'driver:{i} the space is: {nearest_car} KM')
                                                sugges_driv = SuggesDriver(
                                                                    name_customer=c2,
                                                                    driver_name=i,
                                                                    spase_driv_custom=nearest_car,
                                                                    price_trip=price_travel,
                                                                    end_travel=end_l)
                                                sugges_driv.save()
                                    show_service_list = input('do you want to see service list?(yes/no)\n\n')
                                    if show_service_list == 'yes':
                                        cu = Servise.objects.all()
                                        service_list = [x.api() for x in cu]
                                        print(f'list of services:\n\n{list_kardan(service_list)}\n\n')
                                # SAY_COMMENT
                                elif work == '3':
                                    print( )
                                    print(f'list of commentS:\n\n{list_kardan(say_comment)}')
                                    for u in suggestion_driver:
                                        nam_driv = u['driver_name']
                                        say_com = Register_a_comment(
                                            drive_na=nam_driv,
                                            travel_code = random.randint(1,20),
                                            option = input('enter  your opinion:')
                                            )
                                        # say_comment.append(say_com)
                                        say_com.save()
                                        say_comment=say_com.api()
                                        name_dri = say_comment['drive_na']
                                        code_travel = say_comment['travel_code']
                                        opinion = say_comment['option']
                                        print( )
                                        print(f'comment:\n name driver:{name_dri}\n code travel:{code_travel}.\n opinion:{opinion}')
                                else:
                                    break
                        else:
                            print('your code not correct')
                else:
                    break

        # DRIVER
        elif i == '3':
            while True:
                passw = int(input('enter your driver_code or 0 for exit:'))
                for d_c in drivers:
                    driv_code = d_c['driver_code']
                    if passw == driv_code:
                        print('you joined')
                        wallet_dri = d_c['wallet_driver']

                        while True:
                            work_driv = ['axcept_servise', 'servise_fee_request']
                            work_dr = make_list(work_driv)
                            print(work_dr)
                            work_driver = input('enter a number or 0 for exit:')

                            # ACSCEPT_SERVICE
                            if work_driver == '1':
                                for u in suggestion_driver:
                                    v = u['driver_name']

                                    if d_c['name'] in v:
                                        print(f'name_driver:{v}')
                                        print()
                                        print(f'new service: \n{list_making(suggestion_driver)}')

                                        accsept = input('axcept(yes or no)?')
                                        if accsept == 'yes':
                                            print('service cofirmed')
                                        else:
                                            print('you canselled the service')
                                    else:
                                        print('enter a valid value')

                            # SERVICE_FEE_REQUEST
                            elif work_driver == '2':
                                while True:
                                    for u in suggestion_driver:
                                        print(f'suggestion_driver { suggestion_driver}')
                                        v = u['driver_name']

                                        if d_c['name'] in v:
                                            pri_services = ['request_price', 'wallET_driver']

                                            # INFORMATION_SERVICE_NOW
                                            t = make_list(pri_services)
                                            print(f'price_services: \n{t}')
                                            j = input('enter a number or 0 for exit:')

                                            # REQUEST_PRICE_AND_SEND_TO_SNAPP_MANAGER
                                            if j == '1':
                                                for s in suggestion_driver:
                                                    price_service = s['price_trip']
                                                    print(f'price_service is: {price_service}')
                                                    take_price = input('you want to take your money?( yes)')
                                                    if take_price == 'yes':
                                                        print()
                                                        print('Your request has been registered')
                                                        print()

                                                        remaining_money_driver = wallet_dri + price_service

                                                        snapp_driver = Driver.objects.all()
                                                        for j in snapp_driver:
                                                            if j.driver_code == driv_code:
                                                                j.wallet_driver = remaining_money_driver
                                                                j.save()
                                                        print(f'remaining money driver: {remaining_money_driver}')

                                        # WALLET_DRIVER
                                            elif j == '2':
                                                print()
                                                print(f'your wallet is: {wallet_dri}')
                                                print()
                                            else:
                                                break
                                        else:
                                            print('please enter a correct value.')
                                            break
                                    break
                            else:
                                break
                    elif passw != driv_code:
                        print('enter a valid value')
                else:
                    break