from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Author, Book

import wikipedia

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
    isbn = request.POST['isbn']

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
        author.add_bio()
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
        if isbn != '':
            if Book.objects.isbn_exists(isbn):
                msg = "A book with this ISBN has already been inputted."
                payload["msg"] = msg
                payload["status"] = 400
                return JsonResponse(payload)
            else:
                book.isbn = isbn
        book.save()
        
        # Add the Book to the Author's works.
        author.add_to_works(book)
    else:
        msg = "This book has already been logged."
        payload["msg"] = msg
        payload["status"] = 400

    return JsonResponse(payload)

def edit_about_the_author(request):
    payload = {"status": 200}

    author = request.POST['author']
    author_name = author.split()
    author_obj = Author.objects.get(first_name=author_name[0], last_name=author_name[1])

    bio = request.POST['bio']

    author_obj.bio = bio
    author_obj.save()

    return JsonResponse(payload)

def edit_isbn(request):
    payload = {"status": 200}

    book_id = int(request.POST['book'])
    book = Book.objects.get(id=book_id)

    isbn = request.POST['isbn']
    book.isbn = isbn
    book.save()

    return JsonResponse(payload)