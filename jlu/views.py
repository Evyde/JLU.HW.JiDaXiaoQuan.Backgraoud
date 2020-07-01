from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from jlu import models
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import pdb


# Create your views here.


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
        if models.checkUserVoted(i.id, request.GET['openid']):
            url = "/images/star_filled.png"
        rtnData.append({'title': i.passageTitle, 'abstract': i.abstract,
                        'openid': i.createUserOpenID, 'upNum': i.upNum, 'id': i.id,
                        'userinfo': getUserInfo(openid=i.createUserOpenID), 'starurl': url,
                        'createtime': models.getPassageTime(i.id), 'seenusers': i.seenUsersNum,
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
    return JsonResponse(models.checkin(request.GET['openid'], request.GET['locationid'], request.GET['location'], request.GET['loginkey']))


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


@csrf_exempt
def createPassage(request):
    return JsonResponse(models.createPassage(request))


def voteUp(request):
    return JsonResponse(models.voteUp(request.GET['passageid'], request.GET['openid'], request.GET['loginkey']))


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
    p = models.getPassageByID(request.GET['passageid'])
    p.seenUsersNum += 1
    p.save()
    url = "/images/thumb.png"
    if models.checkUserVoted(request.GET['passageid'], request.GET['openid']):
        url = "/images/thumb_filled.png"
    return JsonResponse({'content': p.passageContent,
                         'createtime': models.getPassageTime(request.GET['passageid']),
                         'title': p.passageTitle,
                         'openid': p.createUserOpenID, 'upNum': p.upNum, 'id': p.id,
                         'userinfo': getUserInfo(openid=p.createUserOpenID),
                         'thumburl': url,
                         })


def test(request):
    return HttpResponse("test")


def get_csrf(request):
    # 生成 csrf 数据，发送给前端
    # 弃用，微信小程序不支持Cookie
    x = csrf(request)
    csrf_token = x['csrf_token']
    return JsonResponse({'csrf': csrf_token})


def getUserHistory(request):
    return JsonResponse(models.getUserHistory(request.GET['openid']))
