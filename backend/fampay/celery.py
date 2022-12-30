import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fampay.settings')

app = Celery('fampay')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "sync_task": {
        "task": "ytsync.tasks.load_videos_periodically",
        "schedule": 10.0,
    },
}