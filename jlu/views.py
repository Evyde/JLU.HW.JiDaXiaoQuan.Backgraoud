from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from jlu import models
# Create your views here.


def test(request):
    return HttpResponse(json.dumps({"title":"helloworld"}))


def wxInfo(request):
    rtnData = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" %
    ("wx908d78c4818ee8d3", "75162e79d24afbe90031613e8f6067ce", request.GET['resCode']))
    rtnDataJSON = json.loads(rtnData.text)
    if rtnDataJSON['errcode'] != 0:
        print("ERROR%s" % str(rtnDataJSON['errcode']))
    models.UserInfo.objects.create(openID="aa64sd", nickName="HF", avatarUrl="this")
    return HttpResponse(rtnData.text)