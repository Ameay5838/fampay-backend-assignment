from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import JsonResponse
from django.shortcuts import render

from datetime import datetime
from .models import VideoListing
from .serializers import VideoListingSerializer
# Create your views here.

def get_videos(request):

    if request.method == 'GET':
        publishedBefore = request.GET.get('publishedBefore')

        if not publishedBefore:
            publishedBefore = get_current_date()
        else:
            publishedBefore = transform_date(publishedBefore)
    
        videos = VideoListing.objects.all().filter(publishedAt__lte = publishedBefore)

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
                "data": data
            })
        else:
            return JsonResponse({
                "NOT ENOUGH DATA" : "HAHA"
            })

def search_videos(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        
        if not query:
            return JsonResponse(
                {"message": "Empty query string provided."}
            )

        search_vector = SearchVector('title', 'description')
        search_query = SearchQuery(query)

        res = VideoListing.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(
                search=search_query
            ).order_by(
                '-rank'
            )

        if len(res) == 0:
            return JsonResponse(
                {
                    "message": "No videos found."
                }
            )

        serializer = VideoListingSerializer(res, many=True)
        data = serializer.data

        return JsonResponse({
            "data": data
        })


def get_current_date():
    return datetime.utcnow()

def transform_date(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ').utcnow()