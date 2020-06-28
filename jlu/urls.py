from django.conf.urls import url
from . import views

urlpatterns = [
    url('jlu/wxLogin', views.wxLogin),
    url('jlu/wxCheckSignature', views.checkSignature),
    url('jlu/wxSetUserInfo', views.setUserInfo),
    url('jlu/getAllMarkers', views.getAllMarkers),
    url('jlu/createLocation', views.createLocation),
    url('jlu/getPassages', views.getPassages),
    url('jlu/wxGetUserInfo', views.getUserInfo),
    url('jlu/checkin', views.checkin),
    url('jlu/getAllAnnounce', views.getAllAnnounce),
    url('jlu/getCheckedinLocations', views.getCheckedinLocations),
    url('jlu/createPassage', views.createPassage),
    url('jlu/voteUp', views.voteUp),
    url('jlu/getLocationByID', views.getLocationByID),
]