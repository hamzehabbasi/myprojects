from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from Snapp.models import *
from Snapp.snapp_module import *
# Create your tests here.
# import json

import math

class Snapp():
    snapp_ma=SnappManager.objects.all()
    snapp_ma= [x.api() for x in snapp_ma]
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
                        work_manager = ['register_your_self', 'register_driver', 'pay_service']
                        work_manager = make_list(work_manager)
                        print()
                        print(f'the snapp_manager can do:\n{work_manager}')
                        print()
                        prefer = input('which one wnat to do ?(0 for exit)')
                        if prefer == '1':

                            # SNAPP_MANAGER
                            snapp_manager = SnappManager(
                                code=int(input('enter a code:')),
                                name = input('enter the name:'),
                                familly = input('enter the familly'),
                                addres = input ('enter the addres:'),
                                phone_number = int(input('enter phone_number:')),
                                user_name = input('enter user_name'),
                                password = int(input('password:')),
                            )
                            # print(f'the information of snapp_manager:\n{list_kardan(snapp_ma)}')
                            snapp_ma.append(snapp_manager)
                            snapp_manager.save()

                        # DRIVERS



