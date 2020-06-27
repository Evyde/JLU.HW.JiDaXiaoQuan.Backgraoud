from django.db import models
import requests, json, hashlib


# Create your models here.


class UserInfo(models.Model):
    nickName = models.CharField(max_length=50)
    openID = models.TextField(unique=True, default=0)
    avatarUrl = models.TextField()
    sessionKey = models.TextField()
    gender = models.SmallIntegerField(default=1)


def login(request):
    data = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" %
        ("wx908d78c4818ee8d3", "75162e79d24afbe90031613e8f6067ce", request.GET['resCode']))
    dataJSON = json.loads(data.text)
    if "errcode" in dataJSON.keys():
        return {'openid': dataJSON['openid'], 'errcode': str(dataJSON['errcode'])}
    if len(UserInfo.objects.filter(openID=dataJSON['openid'])) != 0:
        UserInfo.objects.filter(openID=dataJSON['openid']).update(sessionKey=dataJSON['session_key'])
    else:
        UserInfo.objects.create(openID=dataJSON['openid'], sessionKey=dataJSON['session_key'])
    return {'openid': dataJSON['openid'], 'errcode': 0}


def signature(request):
    openID = str(request.GET['openid'])
    s1 = hashlib.sha1(str(str(request.GET['rawData']) + UserInfo.objects.get(openID=openID).sessionKey).encode('utf-8'))
    return str(s1.hexdigest()) == str(request.GET['signature'])


def setUserInfo(request):
    dataJSON = json.loads(str(request.GET['rawData']))
    if signature(request):
        UserInfo.objects.filter(openID=str(request.GET['openid'])).update(
            nickName=dataJSON['nickName'],
            avatarUrl=dataJSON['avatarUrl'],
            gender=dataJSON['gender']
        )
    return {'msg': "Success"}