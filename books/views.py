from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Author, Book

def index(request):
    # First 5 books from alphabetically ordered set.
    books = Book.objects.order_by('title')
    
    # [:5] for first 5

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

def add_book(request):
    payload = {"status": 200}
    msg = ""

    title = request.POST['title']
    author = request.POST['author']
    summary = request.POST['summary']
    image_url = request.POST['image']

    # Split the input into first and last name
    split_name_array = author.split()
    if len(split_name_array) != 2:
        msg = "Make sure author has first and last name."
        payload["status"] = 400
        payload["msg"] = msg
        return JsonResponse(payload)

    first_name = split_name_array[0]
    last_name = split_name_array[1]

    print(first_name, last_name)

    if not Author.objects.author_exists(first_name, last_name):
        # Author does not exist. Create it.
        author = Author.objects.create_author(first_name, last_name)
    else:
        # Author exists. Get it.
        author = Author.objects.get_by_name(first_name, last_name)

    if not Book.objects.book_exists(title, author):
        # Book does not exist. Create it.
        book = Book.objects.create_book(title, author)

        if summary != '':
            book.summary = summary
        if image_url != '':
            book.image_url = image_url
        book.save()
        
        # Add the Book to the Author's works.
        author.add_to_works(book)
    else:
        msg = "This book has already been logged."
        payload["msg"] = msg
        payload["status"] = 400

    return JsonResponse(payload)