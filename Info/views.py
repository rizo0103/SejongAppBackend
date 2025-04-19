from django.shortcuts import render
from django.http import JsonResponse
from .models import Schedule, Announcement

# Create your views here.
def test_api(request):
    """
    GET response: Simple view that responses "Hello, World!" in json format.
    """

    data = {
        "message": "Hello, World!"
    }
    return JsonResponse(data)

def get_all_schedules(request):
    if request.method == "GET":
        schedules = Schedule.objects.all()
        data = []

        for schedule in schedules:
            data.append({
                'group': schedule.group,
                'teacher': schedule.teacher,
                'book': schedule.book,
                "time": schedule.time if schedule.time else [],
            })
            
        return JsonResponse(data, safe=False)

def get_all_announcements(request):
    if request.method == "GET":
        # Assuming you have a model named AnnouncementImage with a field 'image'
        announcements = Announcement.objects.all()
        data = []

        for announcement in announcements:
            data.append({
                "title": announcement.title,
                "content": announcement.content,
                "images": announcement.images,
                "time_posted": announcement.time_posted.strftime("%Y-%m-%d %H:%M:%S"),
                "author": announcement.author,
                "is_active": announcement.is_active,
                "custom_id": announcement.custom_id,
            })
            
        return JsonResponse(data, safe=False)