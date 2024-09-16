# from django.http import JsonResponse
# from django.shortcuts import render
#
# # Create your views here.
# from .models import User, Product, License
#
# from django.shortcuts import render
# def UserViewSet(request):
#     queryset = User.objects.all()
#     user= [x.api() for x in queryset]
#     return JsonResponse(user, safe=False)
#
#
# def index(request):
#     f=render(request, 'index.html')
#     print(f'sssss{f}')
#     return f
