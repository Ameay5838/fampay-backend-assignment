from django.contrib import admin
from django.urls import re_path as url
from .views import get_videos, search_videos


urlpatterns = [
    url('search', search_videos, name='search_videos'),
    url('getvideos', get_videos, name='get_videos'),
]