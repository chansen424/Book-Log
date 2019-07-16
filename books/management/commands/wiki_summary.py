from django.core.management.base import BaseCommand, CommandError
from books.models import Author

import wikipedia

class Command(BaseCommand):
    help = 'Fill all author bios with Wikipedia summaries'

    def handle(self, *args, **options):
        authors = Author.objects.all()
        for author in authors:
            author.bio = wikipedia.summary(str(author))
            author.save()