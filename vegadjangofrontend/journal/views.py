
from django.http import HttpResponse
from django.shortcuts import render


def helloworld(request):
    return HttpResponse("Hello, world.  Here comes Vega.")