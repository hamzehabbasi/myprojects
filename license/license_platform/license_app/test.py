from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import User, Product, License
# from .serializers import UserSerializer, ProductSerializer, LicenseSerializer

def UserViewSet(request):
    queryset = User.objects.all()
    user= [x.api() for x in queryset]
    return JsonResponse(user, safe=False)

def ProductViewSet(request):
    queryset = Product.objects.all()

    product= [x.api() for x in queryset]
    return JsonResponse(product, safe=False)

def LicenseViewSet(request):
    queryset = License.objects.all()
    licenses= [x.api() for x in queryset]
    return JsonResponse(licenses, safe=False)

def index(request):
    f=render(request, 'index.html')
    print(f'sssss{f}')
    return f
# snapp_manager = Product(
#     user=User.objects.get(id=1),
#     license=License.objects.get(id=1),
#     name='ali',
#     description='hamzeha@gmaiid ksdk sdkl.com',
#
# )
# snapp_manager.save()
#
# user = User(
#     username='ali',
#     email='hamzeha@gmail.com',
#
# )
# user.save()
# l=License(
#     user=User.objects.get(id=1),
#     expires_at=datetime.now() + timedelta(hours=24)
# )
# l.save()