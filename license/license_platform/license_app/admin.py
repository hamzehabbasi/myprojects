from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Product, License

admin.site.register(User)
admin.site.register(Product)
admin.site.register(License)
