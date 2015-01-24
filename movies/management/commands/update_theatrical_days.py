from django.core.management import BaseCommand

from movies.maintenance import theatrical_days


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        theatrical_days.update()
