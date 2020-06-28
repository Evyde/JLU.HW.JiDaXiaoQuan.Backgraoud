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
        for i in p:
            rtnData.append({'title': i.passageTitle, 'abstract': i.abstract, 'content': i.passageContent,
                       'openid': i.createUserOpenID, 'upNum': i.upNum, 'id': i.id})
    else:
        p = models.getPassagesByOpenID(request.GET['openid'])
        for i in p:
            rtnData.append({'title': i.passageTitle, 'abstract': i.abstract, 'content': i.passageContent,
                   'openid': i.createUserOpenID, 'upNum': i.upNum, 'id': i.id})
    return HttpResponse(json.dumps(rtnData))


def getUserInfo(request):
    u = models.getUserInfoByOpenID(request.GET['openid'])
    rtnData = {'nickname': u.nickName, 'avatarurl': u.avatarUrl, 'gender': u.gender}
    return JsonResponse(rtnData)


def checkin(request):
    return JsonResponse(models.checkin(request.GET['openid'], request.GET['locationid']))


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
    return JsonResponse(models.voteUp(request.GET['passageID']))
