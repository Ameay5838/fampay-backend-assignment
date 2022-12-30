import django
from celery import shared_task

from .models import VideoListing, APIKey
from .utils import get_default_time_window, fetch_video_data, get_date_string, aggregate_video_data

@shared_task
def load_videos_periodically():
    """
        Load videos periodically and store in postgres.
    """

    try:
        django.db.connection.ensure_connection()
    except:
        print("DB not up yet.")
        return True

    # Loads the default time window : which will start loading videos uploaded in previous minute
    publishedAfter, publishedBefore = get_default_time_window()


    # Loads valid api keys 
    if APIKey.objects.all().filter(exhausted=False).exists():
        valid_keys = APIKey.objects.all().filter(exhausted=False)
    else:
        return "No valid key available add key from django admin."

    # Gets latest publishedAt date from db and sets that as lower bound
    # Ensuring no videos are skipped in case of task failures.
    latest_published_after = VideoListing.objects.first()
    if latest_published_after:
        date = latest_published_after.publishedAt
        publishedAfter = get_date_string(date)


    pageToken = ""
    data = []

    # Checks Valid Keys
    for key_object in valid_keys:
        key = key_object.key

        # Keep loading from data using nextPageToken untill all videos are loaded
        while True:
            res = fetch_video_data(key, publishedAfter, publishedBefore, pageToken)
                
            if res.status_code == 200:
                res = res.json()
                items = res.get('items')
                pageToken = res.get('nextPageToken', "")

                # store data in array
                aggregate_video_data(data, items)
                
                # add videos to db when pageToken is null
                if pageToken == "":
                    VideoListing.objects.bulk_create(data, ignore_conflicts=True)
                    return True
            else:
                break

        # deactivate key if it loading fails
        key_object.exhausted = True
        key_object.save()


    if len(data) != 0:
        VideoListing.objects.bulk_create(data, ignore_conflicts=True)
        return True
    else:
        return False