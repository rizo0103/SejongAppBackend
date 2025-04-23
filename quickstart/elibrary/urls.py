from django.urls import path
from . import views

urlpatterns = [
    path('elibrary/', views.get_all_books, name='get_all_books'),
]
