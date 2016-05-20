from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . import services


def helloworld(request):
    if not request.user.is_authenticated():
        return redirect('/admin')
    return render(request, 'djanapp/myview.html', {
        'username': request.user.username
    })


def aj_get_cases(request):
    cases = services.get_cases()
    return JsonResponse(cases, safe=False)
