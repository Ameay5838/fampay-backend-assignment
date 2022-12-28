import json

import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from os import environ

from celery import shared_task
from .models import VideoListing, APIKey

load_dotenv()

def transform_date(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%SZ')


@shared_task
def load_videos_periodically():
    publishedAfter = (datetime.utcnow() - timedelta(seconds=6000)).isoformat("T") + "Z"
    publishedBefore = (datetime.utcnow()).isoformat("T") + "Z"
    
    valid_keys = APIKey.objects.all().filter(exhausted=False)
    latest_published_after = VideoListing.objects.first()

    if not latest_published_after:
        date = latest_published_after[0].publishedAt
        publishedAfter = (date).isoformat("T") + "Z"


    for key_object in valid_keys:
        key = key_object.key
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
                    "publishedBefore": publishedBefore 
                }
            )
        items = res.json().get('items')

        if res.status_code == 200:
            data = []
            items = res.json().get('items')
                
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
                        channelTitle= snippet['channelTitle'],
                        thumbnailUrls= snippet['thumbnails']
                    )
                )

            VideoListing.objects.bulk_create(data, ignore_conflicts=True)

            return True
        else:
            key_object.exhausted = True
            key_object.save()

    return False