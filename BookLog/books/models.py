from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    writer = models.OneToOneField('Author', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class AuthorManager(models.Manager):
    def create_author(self, first_name, last_name):
        f_name = first_name.lower()
        l_name = last_name.lower()
        return self.create(first_name=f_name, last_name=l_name)

    def get_by_name(self, first_name, last_name):
        f_name = first_name.lower()
        l_name = last_name.lower()
        return self.filter(first_name=f_name, last_name=l_name).first()

    def author_exists(self, first_name, last_name):
        f_name = first_name.lower()
        l_name = last_name.lower()
        return self.filter(first_name=f_name, last_name=l_name).exists()


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    works = models.ManyToManyField(Book)

    objects = AuthorManager()

    def __str__(self):
        f_name = self.first_name.capitalize()
        l_name = self.last_name.capitalize()
        return f_name + ' ' + l_name

    def add_to_works(self, book):
        self.works.add(book)
        self.save()