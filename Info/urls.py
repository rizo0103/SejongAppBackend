from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api, name='test_api'),
    path('schedules/', views.get_all_schedules, name='get_all_schedules'),
]