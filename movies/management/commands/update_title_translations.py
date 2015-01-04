from django.core.management import BaseCommand

from movies.maintenance import title_translations


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        title_translations.update()
