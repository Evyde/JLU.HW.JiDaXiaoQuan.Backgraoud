from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.


def test(request):
    return HttpResponse(json.dumps({"title":"helloworld"}))