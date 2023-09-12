from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles
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
        username = request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
    # Triggering fn in the utils.py file
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 1)
    # Passing the search_query value to the html for showing that in the
    # search bar
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
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
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
