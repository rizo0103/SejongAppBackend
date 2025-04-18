from django.shortcuts import render
from django.http import JsonResponse
from .models import Schedule

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