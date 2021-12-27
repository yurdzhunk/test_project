import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound


def login_page(request):
    return render(request, 'auth.html')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        context = {}
        context['username'] = username
        return render(request, 'csv_creator.html', context)
        #login(request, user)
        #html = '<html><body>It is now %s.</body></html>' % username
        #return HttpResponse(html)
    else:
        return render(request, 'reauth.html')