import csv
import random
import mimetypes

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

result_files_path = 'csv_generator/csv_files/'

columns_names_types = {
    1: 'Name',
    2: 'Surname',
    3: 'Age',
    4: 'Position',
    5: 'Salary',
}

names_values = {
    'Name': ['Jonny', 'Tom', 'Monica', 'Jake', 'Liza'],
    'Surname': ['Adams', 'Rodriguez', 'Bond', 'Verstappen', 'Mask'],
    'Age': (0, 150),
    'Position': ['Junior', 'Middle', 'Senior', 'TechLead', 'CTO'],
    'Salary': (1000, 12000),
}


def random_getter(name):
    if name in ('Name', 'Surname', 'Position'):
        return random.choice(names_values[name])
    if name == 'Age':
        return random.randrange(*names_values[name])
    if name == 'Salary':
        return random.randrange(*names_values[name], 500)


def login_page(request):
    return render(request, 'auth.html')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        context = {}
        context['username'] = username
        return render(request, 'csv_creator.html', context)
        #login(request, user)
        #html = '<html><body>It is now %s.</body></html>' % username
        #return HttpResponse(html)
    else:
        return render(request, 'reauth.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def generate_csv(request):
    rows = request.POST['rows']
    columns = request.POST['columns']
    filename = request.POST['filename']

    path = 'csv_creator/csv_files/'
    filename = path + filename + '.csv'

    columns_numbers = columns.split(',')
    columns_numbers = [int(number) for number in columns_numbers]
    columns_names = [columns_names_types[number][0] for number in columns_numbers]

    with open(filename, 'w', newline='') as write_obj:
        csv_writer = csv.DictWriter(write_obj, columns_names)
        csv_writer.writeheader()

        for i in range(int(rows)):
            dict_to_write = {
                name: random_getter(name)
                for name in columns_names
            }
            csv_writer.writerow(dict_to_write)

        mime_type, _ = mimetypes.guess_type(filename)

        response = HttpResponse(write_obj, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response
