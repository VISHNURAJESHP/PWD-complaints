from django.http import JsonResponse
from .models import Announcement

def announcement_list(request):
    # Delete announcements older than one month
    Announcement.objects.delete_old_announcements()

    # Retrieve remaining announcements
    announcements = Announcement.objects.all().values('news_id', 'content', 'created_at', 'person_assigned_id')
    announcements_list = list(announcements)

    # Return announcements as JSON
    return JsonResponse({'announcements': announcements_list})
