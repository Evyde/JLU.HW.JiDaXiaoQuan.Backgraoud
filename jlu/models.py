from django.db import models
import requests, json, hashlib


# Create your models here.


class User(models.Model):
    nickName = models.CharField(max_length=50)
    openID = models.TextField(unique=True, default=0)
    avatarUrl = models.TextField()
    sessionKey = models.TextField()
    gender = models.SmallIntegerField(default=1)


class Location(models.Model):
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    createUserID = models.BigIntegerField(unique=True)
    createUserOpenID = models.TextField(unique=True)
    name = models.TextField(max_length=100)
    passagesID = models.TextField()
    createTime = models.DateTimeField()
    checkedNum = models.BigIntegerField()
    range = models.FloatField()
    rank = models.FloatField()
    totalScore = models.BigIntegerField()
    totalScorePeople = models.BigIntegerField()
    city = models.TextField()


class Passages(models.Model):
    createUserOpenID = models.TextField(unique=True)
    createUserID = models.BigIntegerField(unique=True)
    picsUrl = models.TextField()
    passageContent = models.TextField(max_length=10240)


def login(request):
    data = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" %
        ("wx908d78c4818ee8d3", "75162e79d24afbe90031613e8f6067ce", request.GET['resCode']))
    dataJSON = json.loads(data.text)
    if "errcode" in dataJSON.keys():
        return {'openid': dataJSON['openid'], 'errcode': str(dataJSON['errcode'])}
    if len(User.objects.filter(openID=dataJSON['openid'])) != 0:
        User.objects.filter(openID=dataJSON['openid']).update(sessionKey=dataJSON['session_key'])
    else:
        User.objects.create(openID=dataJSON['openid'], sessionKey=dataJSON['session_key'])
    return {'openid': dataJSON['openid'], 'errcode': 0}


def signature(request):
    openID = str(request.GET['openid'])
    s1 = hashlib.sha1(str(str(request.GET['rawData']) + User.objects.get(openID=openID).sessionKey).encode('utf-8'))
    return str(s1.hexdigest()) == str(request.GET['signature'])


def setUserInfo(request):
    dataJSON = json.loads(str(request.GET['rawData']))
    if signature(request):
        User.objects.filter(openID=str(request.GET['openid'])).update(
            nickName=dataJSON['nickName'],
            avatarUrl=dataJSON['avatarUrl'],
            gender=dataJSON['gender']
        )
    return {'msg': "Success"}


def isInRange(latitude, longitude):
    pass


def isLocationExist(location):
    pass


def getAllMarkers():
    return Location.objects.filter('id', 'latitude', 'longitude')
