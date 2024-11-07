from django.db import models
from django.utils import timezone
import datetime
from User.models import official

class AnnouncementManager(models.Manager):
    def delete_old_announcements(self):
        one_month_ago = timezone.now() - datetime.timedelta(days=30)
        self.filter(created_at__lt=one_month_ago).delete()

class Announcement(models.Model):
    news_id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=500)
    person_assigned = models.ForeignKey(
        official, on_delete=models.CASCADE, related_name='Official_name', default='null'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Use the custom manager
    objects = AnnouncementManager()