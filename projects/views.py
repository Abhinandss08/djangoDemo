from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


def projects(reque):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(reque, 'projects/projects.html', context)


def parts_(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/parts_.html', {'projects': projectObj})
