from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects, name="projects"),
    path('parts_/<str:pk>/', views.parts_, name="parts"),
]