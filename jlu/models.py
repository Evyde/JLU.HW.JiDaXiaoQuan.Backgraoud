from django.db import models
import requests, json, hashlib, datetime


# Create your models here.


class User(models.Model):
    nickName = models.CharField(max_length=50)
    openID = models.TextField(unique=True, default=0)
    avatarUrl = models.TextField()
    sessionKey = models.TextField()
    gender = models.SmallIntegerField(default=1)
    lastLoginTime = models.DateTimeField(auto_now=True)
    registerTime = models.DateTimeField(auto_now_add=True)
    locations = models.TextField()


class Location(models.Model):
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    createUserOpenID = models.TextField()
    name = models.TextField(max_length=100)
    passagesID = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    checkedNum = models.BigIntegerField(default=0)
    laRange = models.FloatField()
    loRange = models.FloatField()
    rank = models.FloatField(default=0.0)
    totalScore = models.BigIntegerField(default=0)
    totalScorePeople = models.BigIntegerField(default=0)
    city = models.TextField(default="Huhhot")


class Passages(models.Model):
    createUserOpenID = models.TextField()
    locationID = models.BigIntegerField()
    picsUrls = models.TextField()
    passageContent = models.TextField(max_length=10240)
    passageTitle = models.TextField(max_length=100)
    abstract = models.TextField()


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


def getUserInfo(openid):
    return User.objects.get(openID=openid)


def setUserInfo(request):
    dataJSON = json.loads(str(request.GET['rawData']))
    if signature(request):
        try:
            User.objects.filter(openID=str(request.GET['openid'])).update(
                nickName=dataJSON['nickName'],
                avatarUrl=dataJSON['avatarUrl'],
                gender=dataJSON['gender']
            )
        except:
            return {'msg': False}
        else:
            return {'msg': True}


def isInRange(la, lo, testLa, testLo, laRange, loRange):
    if (abs(float(la) - float(testLa)) <= float(laRange)) and (abs(float(lo) - float(testLo)) <= float(loRange)):
        return True
    return False


def isLocationExist(location):
    for i in Location.objects.all().values_list('latitude', 'longitude', 'laRange', 'loRange'):
        if isInRange(location['latitude'], location['longitude'], i[0], i[1], i[2], i[3]):
            return True
    return False


def createLocation(request):
    data = request.GET
    if isLocationExist({'latitude': data['latitude'], 'longitude': data['longitude']}):
        return {'msg': False}
    else:
        Location.objects.create(
            latitude=data['latitude'],
            longitude=data['longitude'],
            createUserOpenID=data['openid'],
            name=data['name'],
            createTime=datetime.datetime.now(),
            laRange=data['laRange'],
            loRange=data['loRange']
        )
        return {'msg': True}


def createPassage(request):
    data = request.GET
    try:
        Passages.objects.create(
        createUserOpenID=data['openid'],
        locationID=data['locationid'],
        passageContent=data['passagecontent']
        )
    except:
        return {'msg': False}
    else:
        return {'msg': True}


def getPassagesByLocation(locationID):
    return Passages.objects.get(locationID=locationID)


def getPassagesByOpenID(openid):
    return Passages.objects.get(createUserOpenID=openid)


def getAllMarkers():
    rtn = []
    for i in Location.objects.all().values_list('id', 'latitude', 'longitude', 'name', 'createTime'):
        rtn.append({'id': i[0], 'latitude': i[1], 'longitude': i[2], 'callout':{'content': i[3]}, 'createTime': str(i[4])})
    return json.dumps(rtn)
