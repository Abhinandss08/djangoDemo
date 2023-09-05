from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    messages.info(request, 'User was logged out!')
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
            # Prompts to the html form where user can
            # modify data once registered
            return redirect('edit-account')
        else:
            # To display an error message when sign-up is messed up
            messages.error(request,
                           'An error has occurred during registration!')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


# To view each developer profiles without editing access
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # All skills that have description
    topSkils = profile.skill_set.exclude(description__exact="")
    # Skills that have no description
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkils,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


# login_required decorator makes sure that the user is logged-in
# then only can access the account page
@login_required(login_url='login')
# Complete access over own profile for authenticated developers
def userAccount(request):
    # To access the logged-in user without any
    # primary key (one-to-one relationship)
    # profile = Profile.objects.get_or_create(user=request.user)
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # To prefill form-fields before editing
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        # To process static images from form-data and instance
        # used to know exactly which profile we need to update
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    context = {}
    return render(request, 'users/skill_form.html', context)
