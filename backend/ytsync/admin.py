from django.contrib import admin
from .models import VideoListing, APIKey
# Register your models here.

@admin.register(VideoListing)
class VideoListingAdmin(admin.ModelAdmin):
    list_display = ['videoId', 'title', 'description', 'publishedAt']

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'details', 'exhausted']
