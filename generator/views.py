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
        login(request, user)
        return HttpResponse('<h1>Logged in</h1>')
    else:
        raise ValidationError('Invalid Login or password')