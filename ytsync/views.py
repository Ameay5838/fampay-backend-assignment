from django.http import JsonResponse
from django.shortcuts import render

from .models import VideoListing
from .serializers import VideoListingSerializer
# Create your views here.

def get_videos(request):

    if request.method == 'GET':
        videos = VideoListing.objects.all()

        total_videos = len(videos)
        page = int(request.GET.get('page', 1))
        start_page_index = (page * 5) - 5
        end_page_index = page * 5
        print(page, type(start_page_index), end_page_index)

        if start_page_index < total_videos:
            
            videos = videos[start_page_index:end_page_index]
            serializer = VideoListingSerializer(videos, many=True)
            data = serializer.data

            return JsonResponse({
                "total_count": total_videos,
                "page_number": 1,
                "next": f"/getvideos?page={page+1}",
                "previous": None if page == 0 else f"/getvideos?page={page-1}",
                "data": data
            })
        else:
            return JsonResponse({
                "NOT ENOUGH DATA" : "HAHA"
            })

def search_videos():
    pass
