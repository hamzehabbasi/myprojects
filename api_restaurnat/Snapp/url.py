from django.urls import path
from . import api_module
from . import restaurant
app_name='restaurant_api'

urlpatterns=[
    path('admin_api/',restaurant.admin_api, name='admin_api'),
    path('food_list_api/',restaurant.food_list_api, name='food_list_api'),
    path('food_reserved_api/', restaurant.food_reserved_api, name='food_reserved_api'),

]