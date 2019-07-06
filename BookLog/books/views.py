from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Author, Book

def index(request):
    # First 5 books from alphabetically ordered set.
    books = Book.objects.order_by('title')[:5]

    return render(
        request,
        'books/index.html',
        {
            'books': books
        }
    )

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(
        request,
        'books/detail.html',
        {'book': book}
    )