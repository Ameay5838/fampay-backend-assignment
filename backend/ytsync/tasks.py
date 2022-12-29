import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from celery import shared_task
from .models import VideoListing, APIKey

load_dotenv()

def transform_date(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ').utcnow()

@shared_task
def load_videos_periodically():
    publishedAfter = (datetime.utcnow().replace(microsecond=0) - timedelta(seconds=60)).isoformat("T") + "Z"
    publishedBefore = (datetime.utcnow().replace(microsecond=0)).isoformat("T") + "Z"
    
    valid_keys = APIKey.objects.all().filter(exhausted=False)
    latest_published_after = VideoListing.objects.first()

    if latest_published_after:
        date = latest_published_after.publishedAt
        publishedAfter = (date.utcnow().replace(microsecond=0)).isoformat("T") + "Z"


    pageToken = ""
    data = []

    for key_object in valid_keys:
        key = key_object.key

        while True:
            res = requests.get(
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

            if res.status_code == 200:
                res = res.json()
                items = res.get('items')
                pageToken = res.get('nextPageToken', "")
                    
                for i in items:
                    videoId = i['id']['videoId']
                    print(videoId)
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
                
                if pageToken == "":
                    break

            else:
                key_object.exhausted = True
                key_object.save()
                break

    if len(data) != 0:
        VideoListing.objects.bulk_create(data, ignore_conflicts=True)
        return True
    else:
        return False