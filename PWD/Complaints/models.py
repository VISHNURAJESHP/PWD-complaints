from django.db import models
from django.utils import timezone
from User.models import User, official

class Complaints(models.Model):

    WORK_STATUS = [
        ('waiting','Waiting'),
        ('working','Working'),
        ('completed','Completed')
    ]

    WING = [
        ('national_highway','National_Highway'),
        ('road','Road'),
        ('buildings','Buildings'),
        ('bridges','Bridges'),
    ]

    complaint_id = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username')
    complaint_details = models.CharField(max_length=500)
    # image = models.FileField()
    complaint_location = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=WORK_STATUS, default='waiting')
    wing = models.CharField(max_length=200, choices=WING)
    person_assigned = models.ForeignKey(official, on_delete=models.CASCADE, related_name='Official_name',default='null')
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.complaint_details

