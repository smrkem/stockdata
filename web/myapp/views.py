from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . import services

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin')
    return render(request, 'myapp/myreactapp.html', {
        'username': request.user.username
    })


def get_items(request):
    items = services.get_items()
    return JsonResponse(items, safe=False)
