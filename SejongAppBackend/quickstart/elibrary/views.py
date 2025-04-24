from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

def get_all_books(request):
    if request.method == "GET":
        books = Book.objects.all()
        data = []

        for book in books:
            data.append({
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'cover': book.cover_id,
                'file': book.file_id,
                'genres': book.genres,
                'published_date': book.published_date,
                'created_at': book.created_at,
            })
    return JsonResponse(data, safe=False)




