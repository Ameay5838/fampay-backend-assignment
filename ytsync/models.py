from django.db import models

# Create your models here.
class VideoListing(models.Model):
    """
        Video Listing Model stores the video data.
    """
    videoId = models.CharField(max_length=100, null=False, unique=True)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    publishedAt = models.DateTimeField(null=False)
    channelTitle = models.CharField(max_length=100, null=False)
    thumbnailUrls = models.JSONField(null=False)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-publishedAt']
        indexes = [
            models.Index(fields=['title'])
        ]