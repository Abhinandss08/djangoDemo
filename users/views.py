from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Profile
from django.contrib.auth.models import User


def loginUser(request):
    # Creating a page variable to render out login page
    page = 'login'
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


def registerUser(request):
    # Creating a page variable for context dictionary
    page = 'register'
    # Creating an instance of imported 'CustomUserCreationForm' and
    # throw it in the context dictionary
    form = CustomUserCreationForm()
    if request.method == 'POST':
        # Obtaining the data from the form
        form = CustomUserCreationForm(request.POST)
        # Validating the form data fields
        if form.is_valid():
            # Hold the user data in a temporary instance before
            # saving it to the backend or processing
            user = form.save(commit=False)
            # To avoid username being case-sensitive
            user.username = user.username.lower()
            # User being saved to database
            user.save()
            # Django way to output messages
            messages.success(request, 'User account is created!')
            login(request, user)
            return redirect('profiles')
        else:
            # To display an error message when sign-up is messed up
            messages.error(request,
                           'An error has occurred during registration!')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


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
