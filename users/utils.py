# Contains helper function for the views.py to minimize complexity
from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles


def searchProfiles(request):
    # The variable that's later on passed into the filter fn
    search_query = ''
    # checks whether we have a search_query from front-end or not
    if request.GET.get('search_query'):
        # To extract the value given from the front-end through 'get' request
        search_query = request.GET.get('search_query')
    # Need to find the skill in the search_query if it nearly matches
    # the name of skill at the model 'Skill'
    skills = Skill.objects.filter(name__icontains=search_query)
    # Using the 'Profile' model-field attributes filters data,
    # the icontains used to not care about case-sensitive and
    # distinct fn to avoid repetition
    # Checks whether the current profile that we are filtering through contains
    # that specific skill
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    return profiles, search_query
