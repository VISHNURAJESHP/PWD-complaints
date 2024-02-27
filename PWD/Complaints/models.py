from django.db import models
from django.utils import timezone

class Compaints(models.Model):

    WORK_STATUS = [
        ('waiting','Waiting'),
        ('working','Working'),
        ('completed','Completed')
    ]

    complaint_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=50)
    complaint_details = models.CharField(max_length=500)
    # image = models.FileField()
    complaint_location = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=WORK_STATUS, default='waiting')
    reason = models.CharField(max_length=500, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

