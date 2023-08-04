from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {'id': '1',
     'movie': 'Inception',
     'nominee': 'Di Caprio'
     },
    {'id': '2',
     'movie': 'Revenent',
     'nominee': 'Di Caprio',
     },
    {
        'id': '3',
        'movie': 'Avengers',
        'nominee': 'RDJ',
    },
]


def projects(request):
    page = 'project'
    number = 12
    context = {'portion': page, 'num': number, 'projects': projectsList}
    return render(request, 'projects/projects.html', context)


def parts_(request, pk):
    projectObj = None
    for i in projectsList:
        if i['id'] == pk:
            projectObj = i
    return render(request, 'projects/parts_.html', {'project': projectObj})
