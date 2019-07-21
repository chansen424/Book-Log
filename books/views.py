from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Author, Book, Collection, Favorites

import wikipedia

def index(request):
    books = Book.objects.order_by('title')

    return render(
        request,
        'books/index.html',
        {
            'books': books,
        }
    )

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    favorited = False

    current_user = request.user
    if current_user.is_authenticated:
        favorites = Favorites.objects.get(owner=current_user)

        if favorites.books.filter(id=book_id).exists():
            favorited = True

        collections = Collection.objects.filter(owner=current_user)

    return render(
        request,
        'books/detail.html',
        {'book': book,
        'favorited': favorited,
        'user_collections': collections
        }
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

@login_required
def add_to_favorites(request):
    payload = {"status": 200}
    current_user = request.user

    book_id = int(request.POST['book'])
    book = Book.objects.get(id=book_id)

    favorites = Favorites.objects.get(owner=current_user)
    favorites.books.add(book)

    return JsonResponse(payload)

@login_required
def remove_from_favorites(request):
    payload = {"status": 200}
    current_user = request.user

    book_id = int(request.POST['book'])
    book = Book.objects.get(id=book_id)

    favorites = Favorites.objects.get(owner=current_user)
    favorites.books.remove(book)

    return JsonResponse(payload)

@login_required
def add_to_existing_collection(request):
    payload = {"status": 200}

    book_id = int(request.POST['book'])

    collection_id = int(request.POST['collection'])
    collection = Collection.objects.get(id=collection_id)

    # Only add if the book is not already in the collection
    if not collection.books.filter(id=book_id).exists():
        book = Book.objects.get(id=book_id)
        collection.books.add(book)

    return JsonResponse(payload)