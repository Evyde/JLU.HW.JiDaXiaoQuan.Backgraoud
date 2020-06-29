from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from jlu import models


# Create your views here.


def test(request):
    return HttpResponse(json.dumps({"title": "helloworld"}))


def wxLogin(request):
    return JsonResponse(models.login(request))


def checkSignature(request):
    return JsonResponse({'isSafe': models.signature(request)})


def setUserInfo(request):
    return JsonResponse(models.setUserInfo(request))


def getAllMarkers(request):
    return HttpResponse(models.getAllMarkers())


def createLocation(request):
    return JsonResponse(models.createLocation(request))


def getPassages(request):
    rtnData = []
    if 'locationid' in request.GET.keys():
        p = models.getPassagesByLocation(request.GET['locationid'])
    else:
        p = models.getPassagesByOpenID(request.GET['openid'])
    for i in p:
        url = "/images/star.png"
        if models.checkUserVoted(i.id, i.createUserOpenID):
            url = "/images/star_filled.png"
        rtnData.append({'title': i.passageTitle, 'abstract': i.abstract,
                        'openid': i.createUserOpenID, 'upNum': i.upNum, 'id': i.id,
                        'userinfo': getUserInfo(openid=i.createUserOpenID), 'starurl': url,
                        })
    if 'sortby' in request.GET.keys():
        if request.GET['sortby'] == "time":
            rtnData.sort(key=lambda e: int(e.__getitem__('id')), reverse=True)
        else:
            rtnData.sort(key=lambda e: int(e.__getitem__('upNum')), reverse=True)
    else:
        rtnData.sort(key=lambda e: int(e.__getitem__('upNum')), reverse=True)
    return HttpResponse(json.dumps(rtnData))


def getUserInfo(request=None, openid=None):
    if openid is None:
        u = models.getUserInfoByOpenID(request.GET['openid'])
        rtnData = {'nickname': u.nickName, 'avatarurl': u.avatarUrl, 'gender': u.gender}
        return JsonResponse(rtnData)
    else:
        u = models.getUserInfoByOpenID(openid)
        rtnData = {'nickname': u.nickName, 'avatarurl': u.avatarUrl, 'gender': u.gender}
        return rtnData


def checkin(request):
    return JsonResponse(models.checkin(request.GET['openid'], request.GET['locationid'], request.GET['location']))


def getAllAnnounce(request):
    return HttpResponse(json.dumps(models.getAllAnnounce()))


def getCheckedinLocations(request):
    locations = models.getCheckedinLocations(request.GET['openid'])
    rtnData = []
    for i in locations:
        rtnData.append({
            'id': str(i.id),
            'name': i.name,
            'num': i.checkedNum,
            'latitude': str(i.latitude),
            'longitude': str(i.longitude)})
    return HttpResponse(json.dumps(rtnData))


def createPassage(request):
    return JsonResponse(models.createPassage(request))


def voteUp(request):
    return JsonResponse(models.voteUp(request.GET['passageid'], request.GET['openid']))


def getLocationByID(request):
    l = models.getLocationByID(request.GET['locationid'])
    rtnData = {
        'latitude': l.latitude,
        'longitude': l.longitude,
        'createUseropenid': l.createUserOpenID,
        'name': l.name,
        'checkednum': l.checkedNum,
        'larange': l.laRange,
        'lorange': l.loRange,
        'rank': l.rank,
        'totalscore': l.totalScore,
        'totalscorepeople': l.totalScorePeople,
        'city': l.city,
        'id': l.id
    }
    return JsonResponse(rtnData)


def getPassageContent(request):
    return JsonResponse({'content': models.getPassageContent(request.GET['passageid'])})
