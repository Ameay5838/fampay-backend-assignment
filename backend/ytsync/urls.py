from django.contrib import admin
from django.urls import re_path as url
from .views import get_videos


urlpatterns = [
    url('getvideos', get_videos, name='get_videos'),
    url(r'admin/', admin.site.urls), 
]