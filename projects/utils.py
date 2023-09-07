from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    # It's used to retrieve a query parameter named 'page'
    # from the URL's query string.
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    # When user visits the projects page for the first time
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # When user seeks for index beyond last page throws the last page
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # Creating a certain number of page buttons to the left
    leftIndex = (int(page) - 4)
    # When leftIndex value goes way below 1 to reset to first page
    if leftIndex < 1:
        leftIndex = 1
    # Creating a certain number of page buttons to the right
    rightIndex = (int(page) + 5)
    # When rightIndex value goes way beyond max value to reset to last page
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    return custom_range, projects


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tag__in=tags)
    )
    return projects, search_query
