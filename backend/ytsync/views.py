from django.http import JsonResponse

from rest_framework import status

from .models import VideoListing
from .serializers import VideoListingSerializer


from .utils import (
    get_params_data,
    get_pagination_details,
)
# Create your views here.

def get_videos(request):
    """
        Implements fetching videos in reverse chronological order.
        1. Uses publishedBefore and publishedAfter as cursor,
           Both fields are not required only used for making more precise queries.
        2. Fetches page based on page param provided in query.
        3. Page size is 10.
    """
    if request.method == 'GET':
        page, publishedBefore, publishedAfter = get_params_data(request)
        
        videos = VideoListing.objects.all().filter(
            publishedAt__lte = publishedBefore, 
            publishedAt__gte = publishedAfter
        )

        total_videos, start_page_index, end_page_index = get_pagination_details(page, videos)

        if start_page_index < total_videos:
            
            videos = videos[start_page_index:end_page_index]
            serializer = VideoListingSerializer(videos, many=True)
            data = serializer.data

            return JsonResponse(
                {
                    "total_count": total_videos,
                    "page_number": page,
                    "data": data
                },
                status=200
            )
        else:
            return JsonResponse(
                {"message": "No data found."},
                status=404
            )

def search_videos(request):
    """
        Implements search endpoint with postgres full text search feature.
        1. Builds search result using SearchVector on title and description,
           And ranks them according to relevance.
        2. Uses GIN Index internally to speed up search.
    """
    if request.method == 'GET':
        query = request.GET.get('q')
        
        if not query:
            return JsonResponse(
                {"message": "Empty query string provided."},
                status=406
            )

        res = VideoListing.objects.filter(searchvector=query)

        if len(res) == 0:
            return JsonResponse(
                {
                    "message": "No videos found."
                },
                status=404,
            )

        serializer = VideoListingSerializer(res, many=True)
        data = serializer.data

        return JsonResponse(
            {
                "data": data
            },
            status=200
        )
