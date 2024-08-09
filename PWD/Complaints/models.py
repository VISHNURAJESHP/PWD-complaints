from django.db import models
from django.utils import timezone
from User.models import User, official

class Complaints(models.Model):

    WORK_STATUS = [
        ('waiting','Waiting'),
        ('working','Working'),
        ('completed','Completed')
    ]

    complaint_id = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username')
    complaint_details = models.CharField(max_length=500)
    # image = models.FileField()
    complaint_location = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=WORK_STATUS, default='waiting')
    reason = models.CharField(max_length=500, null=True)
    person_updated = models.ForeignKey(official, on_delete=models.CASCADE, related_name='Official_name')
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

