from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Groups
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

def get_all_users(request):
    if request.method == "GET":
        users = User.objects.all()
        data = []

        for user in users:
            data.append({
                'username': user.username,
                'fullname': user.fullname,
                'email': user.email,
                'phone_number': user.phone_number,
                'status': user.status,
                'groups': user.get_groups(),
                'avatar': user.avatar_id,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            })

    return JsonResponse(data, safe=False)


def get_all_groups(request):
    if request.method == "GET":
        groups = Groups.objects.all()
        data = []

        for group in groups:
            data.append({
                'name': group.name,
                'created_at': group.created_at,
                'user_count': group.user_count(),
                'participants': group.participant_names(),
            })
    return JsonResponse(data, safe=False)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Декодируем и парсим JSON
            username = data['username'] if 'username' in data else None
            password = data['password'] if 'password' in data else None
            if (not username) or (not password):
                return JsonResponse({'error': 'Please send correct data'})

            user = authenticate(request, username = username, password = password)
            if user:
                return JsonResponse({"user_data": {
                    "username": user.username,
                    "group": user.get_groups(),
                    "fullname": user.fullname,
                    "email":user.email,
                    "phone_number": user.phone_number,
                    "avatar": user.avatar_id
                }})
            else:
                return JsonResponse({"error": "user not found"})
        except Exception as e:
            return JsonResponse({"ERROR": str(e)})
    return JsonResponse({"message": "post requests allowed only"})