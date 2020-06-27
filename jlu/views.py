from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import json
from jlu import models
# Create your views here.


def test(request):
    return HttpResponse(json.dumps({"title":"helloworld"}))


def wxLogin(request):
    return JsonResponse(models.login(request))


def checkSignature(request):
    return JsonResponse({'isSafe': models.signature(request)})


def setUserInfo(request):
    return JsonResponse(models.setUserInfo(request))