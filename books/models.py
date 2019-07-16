from django.db import models
import wikipedia

# Create your models here.
class BookManager(models.Manager):
    def create_book(self, title, writer=None):
        # Every word in a title should be capitalized for consistent formatting.
        formatted_title = self.format_book_title(title)

        if writer is None:
            return self.create(title=formatted_title)
        
        return self.create(title=formatted_title, writer=writer)
    
    def format_book_title(self, title):
        formatted_title = ''

        title_array = title.split()
        for word in title_array:
            temp = ' ' + word.capitalize()
            formatted_title += temp

        return formatted_title

    def book_exists(self, title, writer):
        formatted_title = self.format_book_title(title)
        return self.filter(title=formatted_title, writer=writer).exists()

    def isbn_exists(self, isbn):
        return self.filter(isbn=isbn).exists()

    def get_book(self, title, writer):
        formatted_title = self.format_book_title(title)
        return self.filter(title=formatted_title, writer=writer).first()

class Book(models.Model):
    title = models.CharField(max_length=100, unique=False)
    writer = models.ForeignKey('Author', on_delete=models.CASCADE, default=None)
    summary = models.CharField(max_length=300, default="")
    image_url = models.URLField(null=True, default=None)
    isbn = models.CharField(max_length=13, default="")


    objects = BookManager()

    def __str__(self):
        return self.title


class AuthorManager(models.Manager):
    def create_author(self, first_name, last_name):
        # First and last name should be capitalized for consistent formatting.
        f_name, l_name = self.format_author_name(first_name, last_name)
        return self.create(first_name=f_name, last_name=l_name)

    def format_author_name(self, first_name, last_name):
        return first_name.capitalize(), last_name.capitalize()

    def get_by_name(self, first_name, last_name):
        f_name, l_name = self.format_author_name(first_name, last_name)
        return self.filter(first_name=f_name, last_name=l_name).first()

    def author_exists(self, first_name, last_name):
        f_name, l_name = self.format_author_name(first_name, last_name)
        return self.filter(first_name=f_name, last_name=l_name).exists()


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    works = models.ManyToManyField(Book)
    bio = models.CharField(max_length=500, default="")

    objects = AuthorManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def add_to_works(self, book):
        self.works.add(book)
        self.save()

    def add_bio(self):
        self.bio = wikipedia.summary(str(self))
        self.save()