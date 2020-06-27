from django.conf.urls import url
from . import views

urlpatterns = [
    url('jlu/wxLogin', views.wxLogin),
    url('jlu/wxCheckSignature', views.checkSignature),
    url('jlu/wxSetUserInfo', views.setUserInfo)
]