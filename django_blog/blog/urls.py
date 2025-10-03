# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'  # Namespace for the blog app

urlpatterns = [
    path('', views.home, name='home'),  # Home page for the blog
]