from django.core.management import BaseCommand

from movies.maintenance import localizations


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        localizations.update()
