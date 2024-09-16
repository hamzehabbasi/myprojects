from django.db import models
from django.utils import timezone
import random
import datetime
# Create your models here.
import random
import datetime


# Create your models here.

class SnappManager(models.Model):
    code = models.IntegerField(null=False)
    name = models.CharField(max_length=250, null=False)
    familly = models.CharField(max_length=250)
    addres = models.CharField(max_length=250)
    phone_number = models.IntegerField(default=0)
    user_name = models.CharField(max_length=250)
    password = models.IntegerField(default=0)

    def api(self):
        return {
            "code": self.code,
            "name": self.name,
            "familly": self.familly,
            "addres": self.addres,
            "phone_number": self.phone_number,
            "user_name": self.user_name,
            "password": self.password
        }

class Customer(models.Model):
    customer_code = models.IntegerField(default=0)
    name = models.CharField(max_length=250)
    familly = models.CharField(max_length=250)
    addres = models.CharField(max_length=250)
    phone_number = models.IntegerField(default=0)
    location_driv = models.CharField(max_length=250, default=0)
    wallet_customer = models.IntegerField(default=0)

    #     self.location_driv = random.randint(100, 1000)
    def api(self):
        return {
            "customer_code": self.customer_code,
            "name": self.name,
            "familly": self.familly,
            "addres": self.addres,
            "phone_number": self.phone_number,
            "location_driv": self.location_driv,
            'wallet_customer': self.wallet_customer
        }

class Transaction(models.Model):
    customer_name= models.CharField(max_length=250)
    transaction_code = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField(default=0)
    bank = models.CharField(max_length=250)
    traking_code = models.IntegerField(default=0)

    def api(self):
        return {
            "customer_name": self.customer_name,
            "transaction_code": self.transaction_code,
            "date": self.date,
            "price": self.price,
            "bank": self.bank,
            "traking_code": self.traking_code
        }

class Driver(models.Model):
    manager_code = models.CharField(max_length=250)
    driver_code = models.IntegerField(default=0)
    name = models.CharField(max_length=250)
    familly = models.CharField(max_length=250)
    phone_number = models.IntegerField(default=0)
    address = models.CharField(max_length=250)
    national_code = models.IntegerField(default=0)
    model_car = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    plaque_car = models.IntegerField(default=0)
    location_driv = models.IntegerField(default=0)
    wallet_driver=models.IntegerField(default=0)

    def api(self):
        return {
            "manager_code": self.manager_code,
            "driver_code": self.driver_code,
            "name": self.name,
            "familly": self.familly,
            "phone_number": self.phone_number,
            "location_driv": self.location_driv,
            "national_code": self.national_code,
            "address": self.address,
            "model_car": self.model_car,
            "color": self.color,
            "plaque_car": self.plaque_car,
            'wallet_driver':self.wallet_driver
        }

    @property
    def manager_code_driver(self):
        return self.manager_code.code

class Service_charge(models.Model):
    manager_code = models.CharField(max_length=250, default=0)
    driver_co = models.CharField(max_length=250, default=0)
    service_charg_code = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField(default=0)
    tracking_code = models.IntegerField(default=0)

    def api(self):
        return {
            # 'manager_code': self.manager_code,
            'drive': self.driver_co,
            'service_charg_code': self.service_charg_code,
            'date': self.date,
            'price': self.price,
            'tracking_code': self.tracking_code,
        }

class Servise(models.Model):
    drive_nam = models.CharField(max_length=250, default=0)
    plaq_car = models.CharField(max_length=250, default=0)
    customer_name = models.CharField(max_length=250, default=0)
    location_start = models.IntegerField(default=0)
    location_end = models.IntegerField(default=0)
    price_travel = models.IntegerField(default=0)
    registration_date = models.DateTimeField(default=timezone.now)

    def api(self):
        return {
            'drive_nam': self.drive_nam,
            'plaque_car': self.plaq_car,
            'customer_name': self.customer_name,
            'location_start': self.location_start,
            'location_end': self.location_end,
            'price_travel': self.price_travel,
            'registration_date': self.registration_date,
        }
class SuggesDriver(models.Model):
    name_customer=models.CharField(max_length=250, default=0)
    driver_name=models.CharField(max_length=250, default=0)
    spase_driv_custom=models.IntegerField(default=0)
    price_trip=models.IntegerField(default=0)
    end_travel=models.IntegerField(default=0)

    def api(self):
        return {
            'name_customer': self.name_customer,
            'driver_name': self.driver_name,
            'spase_driv_custom': self.spase_driv_custom,
           'price_trip': self.price_trip,
            'end_travel': self.end_travel
        }

class Register_a_comment(models.Model):
    drive_na = models.CharField(max_length=250, default=0)
    travel_code = models.IntegerField(default=0)
    option = models.CharField(max_length=250)

    def api(self):
        return {
            'drive_na': self.drive_na,
            'travel_code': self.travel_code,
            'option': self.option,
        }

class Location(models.Model):
    lenght = models.IntegerField(default=0)
    width = models.IntegerField(default=0)

    def api(self):
        # return [self.lenght, self.width]
        return {
            'lenght': self.lenght,
            'width': self.width,
        }
