from rest_framework import serializers
from .models import VideoListing


class VideoListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoListing
        fields = ('videoId', 'title', 'description', 'publishedAt', 'channelTitle', 'thumbnailUrls')
        