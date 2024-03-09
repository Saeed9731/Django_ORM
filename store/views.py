from django.shortcuts import render
from django.http import HttpResponse

def say_welcome(request, name):
    return render(request, 'hello.html', {
        "name": name
    })

def say_goodby(request):
    return HttpResponse('Goodby')

def say_number(request):
    return HttpResponse('This is just number!!')

def say_something(request, num):
    return render(request, 'say_something.html', {
        'num': num,
    })
