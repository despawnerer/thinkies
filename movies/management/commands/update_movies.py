from django.core.management import BaseCommand

from movies.maintenance import movie_import


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        movie_import.update()
