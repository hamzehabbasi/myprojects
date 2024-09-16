# from django.conf.urls import url
# from django.contrib import admin
#
# from boards import views

# urlpatterns = [
#     url(r'^$', views.home, name='home'),
#     url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
#     url(r'^admin/', admin.site.urls),]
from django.urls import path
from . import views
from .models import Inform
name_app='app'
urlpatterns=[
    path('inform/',views.say_inform),
    path('home/', views.home),
]
