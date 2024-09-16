from django.shortcuts import render
from .models import Inform
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('home is here')
#     all=Inform.objects.all()
#     return render(request, 'home.html',{'all':all})


def say_inform(request):
    return HttpResponse('Hello User...')
    # all=Inform.objects.all()
    # return render(request, 'hello.html', {'all': all})
