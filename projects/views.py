from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


def parts_(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/parts_.html', {'projects': projectObj})


@login_required(login_url='login')
def createProject(request):
    # To get the currently logged-in user
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # To get the instance of the current project
            project = form.save(commit=False)
            # To get an owner connected to a profile model and to track
            # the recently added project in account section
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def updateProject(request, pk):
    profile = request.user.profile
    # Querying the logged-in user's profile and getting
    # all the children (projects), thus updating the project
    # limited to the logged-in owner
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)
