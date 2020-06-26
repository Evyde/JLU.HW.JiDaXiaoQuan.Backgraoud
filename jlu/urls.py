from django.conf.urls import url
from . import views

urlpatterns = [
    url('jlu/wxlogin', views.wxInfo)
]