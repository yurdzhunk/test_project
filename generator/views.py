import json

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound


def login_user(request):
    params = json.loads(request.body)
    username = params['username']
    password = params['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('<h1>Logged in</h1>')
    else:
        raise ValidationError('Invalid Login or password')