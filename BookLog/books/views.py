from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

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

def add_book(request):
    title = request.POST['title']
    
    author = request.POST['author']

    # Split the input into first and last name
    split_name_array = author.split()
    first_name = split_name_array[0]
    last_name = split_name_array[1]

    if not Author.objects.author_exists(first_name, last_name):
        # Author does not exist. Create it.
        author = Author.objects.create_author(first_name, last_name)
    else:
        # Author exists. Get it.
        author = Author.objects.get_by_name(first_name, last_name)

        # TODO: Check if a book by that title from this author exists.
        # If it does, redirect or raise an error

    # Create Book
    book = Book.objects.create(title=title, writer=author)

    # Add the Book to the Author's works.
    author.add_to_works(book)

    return HttpResponseRedirect(reverse('books:index'))