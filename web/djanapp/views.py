from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from . import services


def helloworld(request):
    return render(request, 'djanapp/myview.html')


def aj_get_cases(request):
    cases = services.get_cases()
    return JsonResponse(cases, safe=False)
