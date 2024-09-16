import random
from Snapp.models import *
from django.http import HttpResponse
from Snapp.api_module import *

def admin_api(request):
    admin = AdminRestaurant.objects.all()
    admin = [x.api() for x in admin]
    return HttpResponse(admin)

def food_list_api(request):
    food_list=foods_list.objects.all()
    food_list= [x.api() for x in food_list]
    return HttpResponse(food_list)

def food_reserved_api(request):
    food_reserved = Food_reseved.objects.all()
    food_reserved = [x.api() for x in food_reserved]
    return HttpResponse(food_reserved)

class Restaurant():
    admin=AdminRestaurant.objects.all()
    admin= [x.api() for x in admin]

    food_list=foods_list.objects.all()
    food_list= [x.api() for x in food_list]

    food_reserved = Food_reseved.objects.all()
    food_reserved = [x.api() for x in food_reserved]

    w=input('1=admin. 2= customer')
    if w=='1':
        a=input('join a new admin. 2=join a new food 3=see list reserved foods. 4=list_foods')
        if a== '1':
            admin_name = input('enter the name:')
            admin_number = int(input('enter phone_number:'))
            password = int(input('password:'))
            # ADMIN_MANAGER
            manager = AdminRestaurant(
                admin_name=admin_name,
                admin_number=admin_number,
                password=password,
            )
            # admin.append(manager)
            manager.save()
        elif a == '2':
            food_name = input('enter food name:')
            price_food = int(input('enter price:'))
            food = foods_list(
                name_food=food_name,
                price_foo=price_food,
            )
            # admin.append(manager)
            food.save()

        elif a=='3':
            food_rese=list_kardan(food_reserved)
            print(f'list of food reserved: \n{food_rese}')

        else:
            food_menu=list_kardan(food_list)
            print()
            print(f'food,s menu is:\n{food_menu}')
    # CUSTOMER
    else:
        c=input('1=foods list and reserve. 2=delete')
        if c =='1':
            while True:
                food_menu=make_list(food_list)
                print()
                print(f'food,s menu is:\n{food_menu}')
                choice_food=input('please enter the name of food you want to reserve:(0=exit)')
                if choice_food == '0':
                    break
                for food in food_list:
                    if choice_food == food['name_food']:
                        food_na=choice_food
                        pric_f=food['price_foo']
                        food=Food_reseved(
                            food_name=food_na,
                            food_price=pric_f,
                            food_code=random.randint(100,500)
                            )
                        food.save()
                        print()
                        print(f'your request has been registered and will be ready in 30 minutes')
                        food=Food_reseved.objects.all()
                        f_r=[x.api() for x in food]
                        print(f'list of your reserve_foods:\n{f_r}')
                        print()
                        more=input('do you want more food?(yes=1,no=2)')
                        if more == '1':
                            break
                        else:
                            print('ok, Than you please wait')
                            pass
        elif c == '2':
            print(f'list of your reserve_foods:\n{food_reserved}')
            print()
            d=input('which food want to delete(enter the name)?')
            for res_food in food_reserved:
                if d== res_food['food_name']:
                    res_food.delete()