from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField  
from django.db import models

# Create your models here.
class VideoListing(models.Model):
    """
        Video Listing Model stores the video data.
    """
    videoId = models.CharField(max_length=200, null=False, unique=True)
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    publishedAt = models.DateTimeField(null=False)
    thumbnailUrls = models.JSONField(null=False)
    search_vector = SearchVectorField(null=True) 

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-publishedAt']
        indexes = (
            models.Index(fields=['publishedAt']),
            GinIndex(fields=['search_vector'])
        )

class APIKey(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=200,null=True)
    key = models.TextField()
    exhausted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
