from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    writer = models.OneToOneField('Author', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class AuthorManager(models.Manager):
    def create_author(self, first_name, last_name):
        return self.create(first_name=first_name, last_name=last_name)

    def get_by_name(self, first_name, last_name):
        return self.filter(first_name=first_name, last_name=last_name).first()


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    works = models.ManyToManyField(Book)

    objects = AuthorManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name