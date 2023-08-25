from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User


def loginUser(request):
    # Checks whether user is already authenticated or not
    # and redirects to profile accordingly
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        # Taking username and password values if method is post
        username = request.POST['username']
        password = request.POST['password']
        try:
            # Verifying username present in database
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        # Either returns user object if data matches or returns None if fails
        user = authenticate(request, username=username, password=password)
        # If user is found creates a session and redirects to homepage
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is incorrect !')
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    print(context)
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkils = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkils,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)
