from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Groups
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.models import Token

# def get_all_users(request):
#     if request.method == "GET":
#         users = User.objects.all()
#         data = []

#         for user in users:
#             data.append({
#                 'username': user.username,
#                 'fullname': user.fullname,
#                 'email': user.email,
#                 'phone_number': user.phone_number,
#                 'status': user.status,
#                 'groups': user.get_groups(),
#                 'avatar': user.avatar_id,
#                 'date_joined': user.date_joined,
#                 'is_active': user.is_active,
#                 'is_staff': user.is_staff,
#                 'is_superuser': user.is_superuser,
#             })

#     return JsonResponse(data, safe=False)

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
                token = Token.objects.get(user=user)
                return JsonResponse({"token": token.key})
                # return JsonResponse({"user_data": {
                #     "avatar": user.avatar_id,
                #     "username": user.username,
                #     "fullname": user.fullname,
                #     "phone_number": user.phone_number,
                #     "email":user.email,
                #     'status': user.status,
                #     "group": user.get_groups(),
                # }})
            else:
                return JsonResponse({"error": "user not found"})
        except Exception as e:
            return JsonResponse({"ERROR": str(e)})
    return JsonResponse({"message": "Only POST requests are allowed"})

def change_username(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            new_username = data.get("new_password")

            if not new_username:
                return JsonResponse({"error": "Username is required"}, status=400)
            
            if User.objects.filter(username = new_username).exists():
                return JsonResponse({"error": "Username already taken"})
            
            user = request.user
            user.username = new_username
            user.save()
            return JsonResponse({"message": "Username updated successfully", "new_password": new_username})

        except Exception as e:
            return JsonResponse({"ERROR": str(e)})
        
    return JsonResponse({"error": "Only POST requests are allowed"})

def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            new_password = data.get("new_password")

            if not new_password:
                return JsonResponse({"error": "Password is required"}, status=400)
            
            user = request.user
            user.password = new_password
            user.save()
            return JsonResponse({"message": "Password updated successfully", "new_password": new_password})

        except Exception as e:
            return JsonResponse({"ERROR": str(e)})
        
    return JsonResponse({"error": "Only POST requests are allowed"})