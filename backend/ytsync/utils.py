import requests
from datetime import datetime, timedelta
from .models import VideoListing

def fetch_video_data(key, publishedAfter, publishedBefore, pageToken):
    return requests.get(
        url='https://www.googleapis.com/youtube/v3/search',
        params={
                "part": "id,snippet",
                "type": "video",
                "order": "date",
                "maxResults": 50,
                "q": "football",
                "key": key,
                "publishedAfter": publishedAfter,
                "publishedBefore": publishedBefore,
                "pageToken": pageToken
            }
        )

def get_date(second_delta=60):
    return (datetime.utcnow().replace(microsecond=0) - timedelta(seconds=second_delta)).isoformat("T") + "Z"

def transform_date(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ').utcnow()

def get_date_string(date):
    return (date.utcnow().replace(microsecond=0)).isoformat("T") + "Z"

def get_default_time_window():
    publishedAfter = (datetime.utcnow().replace(microsecond=0) - timedelta(seconds=60)).isoformat("T") + "Z"
    publishedBefore = (datetime.utcnow().replace(microsecond=0)).isoformat("T") + "Z"

    return publishedAfter, publishedBefore

def get_current_date():
    return datetime.utcnow()

def get_oldest_date():
    return datetime.utcnow().min
    
def transform_date(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ').utcnow().replace(microsecond=0)

def get_pagination_details(page, videos_query_set):
    total_videos = len(videos_query_set)
    start_page_index = (page * 10) - 10
    end_page_index = page * 10

    return total_videos, start_page_index, end_page_index
    
def get_params_data(request):
    page = int(request.GET.get('page', 1))
    publishedBefore = request.GET.get('publishedBefore')
    publishedAfter = request.GET.get('publishedAfter')

    if not publishedBefore:
        publishedBefore = get_current_date()
    else:
        publishedBefore = transform_date(publishedBefore)
    
    if not publishedAfter:
        publishedAfter = get_oldest_date()
    else:
        publishedAfter = transform_date(publishedAfter)

    return page, publishedBefore, publishedAfter

def aggregate_video_data(data, items):
    for i in items:
        videoId = i['id']['videoId']
        snippet = i['snippet']
        data.append(
            VideoListing(   
                videoId=videoId,
                title= snippet['title'],
                description= snippet['description'],
                publishedAt= transform_date(snippet['publishedAt']),
                thumbnailUrls= snippet['thumbnails'],
            )
        )

