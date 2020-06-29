from django.db import models
import requests, json, hashlib, datetime
from jlu import utils


# Create your models here.
# 注释：快写完了才发现可以使用多对多、多对一和一对多关系，比我自己设计的方法方便很多


class User(models.Model):
    nickName = models.CharField(max_length=50)
    openID = models.TextField(unique=True, default=0)
    avatarUrl = models.TextField()
    sessionKey = models.TextField()
    gender = models.SmallIntegerField(default=1)
    lastLoginTime = models.DateTimeField(auto_now=True)
    registerTime = models.DateTimeField(auto_now_add=True)
    checkedinLocations = models.ManyToManyField(to="Location")


class Location(models.Model):
    latitude = models.FloatField(unique=True)
    longitude = models.FloatField(unique=True)
    createUserOpenID = models.TextField()
    name = models.TextField(max_length=100)
    passages = models.ManyToManyField(to="Passages")
    createTime = models.DateTimeField(auto_now_add=True)
    checkedNum = models.BigIntegerField(default=0)
    laRange = models.FloatField()
    loRange = models.FloatField()
    rank = models.FloatField(default=0.0)
    totalScore = models.BigIntegerField(default=0)
    totalScorePeople = models.BigIntegerField(default=0)
    city = models.TextField(default="Huhhot")
    checkedUsers = models.ManyToManyField(to="User")


class Passages(models.Model):
    createUserOpenID = models.TextField()
    locationID = models.BigIntegerField()
    passageContent = models.TextField(max_length=10240)
    passageTitle = models.TextField(max_length=100)
    abstract = models.TextField()
    upNum = models.BigIntegerField(default=0)
    pic = models.ImageField()
    starUsers = models.ManyToManyField(to="User")


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
        l = Location(
            latitude=data['latitude'],
            longitude=data['longitude'],
            createUserOpenID=data['openid'],
            name=data['name'],
            createTime=datetime.datetime.now(),
            laRange=data['laRange'],
            loRange=data['loRange']
        )
        l.save()
        User.objects.get(openID=data['openid']).checkedinLocations.add(l)
        l.checkedNum += 1
        l.save()
        return {'msg': True}


def createPassage(request):
    data = request.GET
    try:
        p = Passages(
            createUserOpenID=data['openid'],
            locationID=data['locationid'],
            passageTitle=data['passagetitle'],
            passageContent=data['passagecontent'],
            abstract=data['passagecontent'][0:50]
        )
        p.save()
        Location.objects.get(id=data['locationid']).passages.add(p)
    except:
        return {'msg': False}
    else:
        return {'msg': True}


def getPassagesByLocation(locationID):
    return Passages.objects.filter(locationID=locationID).all()


def getPassagesByOpenID(openid):
    return Passages.objects.filter(createUserOpenID=openid).all()


def getAllMarkers():
    rtn = []
    for i in Location.objects.all().values_list('id', 'latitude', 'longitude', 'name', 'createTime'):
        rtn.append(
            {'id': i[0], 'latitude': i[1], 'longitude': i[2], 'iconPath':'/images/marker.png','callout': {'content': i[3],
                'fontSize': 15,'borderRadius': 1,'textAlign':'center',
      'padding':5}, 'width': "50px", 'height': "50px",'createTime': str(i[4])})
    return json.dumps(rtn)


def getUserInfoByOpenID(openid):
    return User.objects.get(openID=openid)


def checkin(openid, locationid, location):
    location = json.loads(location)
    for i in User.objects.get(openID=openid).checkedinLocations.all():
        if i is not None:
            if i.id == int(locationid):
                return {'msg': False}
    l = Location.objects.get(id=locationid)
    if isInRange(l.latitude, l.longitude, location['latitude'], location['longitude'], l.laRange, l.loRange):
        l.checkedUsers.add(User.objects.get(openID=openid))
        User.objects.get(openID=openid).checkedinLocations.add(Location.objects.get(id=locationid))
        l.checkedNum += 1
        l.save()
        return {"msg": True}
    else:
        return {'msg': False}


def getAllAnnounce():
    tmp = utils.GetAnnounce()
    tmp.createCache()
    return tmp.get()


def getCheckedinLocations(openid):
    return User.objects.get(openID=openid).checkedinLocations.all()


def checkUserVoted(passageid, openid):
    us = Passages.objects.get(id=passageid).starUsers
    u = User.objects.get(openID=openid)
    try:
        for i in us:
            if i is u:
                return True
    except:
        pass
    return False


def voteUp(passageid, openid):
    try:
        u = User.objects.get(openID=openid)
        p = Passages.objects.get(id=passageid)
        pu = p.starUsers
        if pu:
            for i in pu:
                if i is u:
                    return {'msg': False}
        p.upNum += 1
        p.starUsers.add(User.objects.get(openID=openid))
        p.save()
    except:
        return {'msg': False}
    return {"msg": True}


def getLocationByID(locationid):
    return Location.objects.get(id=locationid)


def getPassagePic(passageid):
    return Passages.objects.get(id=passageid).pic


def getPassageContent(passageid):
    return Passages.objects.get(id=passageid).passageContent
