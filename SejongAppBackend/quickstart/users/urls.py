from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.get_all_groups, name='get_all_groups'),
    path('login/', views.login_view, name='login_view'),
]
