from django.shortcuts import render
from django.http import HttpResponse


def projects(request):
    return render(request,'projects.html')


def parts_(request, pk):
    return render(request,'parts_.html')
