import logging
import csv
import os
import dateutil.parser
from funcy import chunks, cached_property

from django.db import transaction
from django.conf import settings

from ..models import Movie


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    total = 0
    for chunk in chunks(1000, get_all_movie_items()):
        with transaction.atomic():
            for item in chunk:
                update_item(item)
                total += 1
        logger.info("Updated %d movies" % total)
    logger.info("Finished")


@transaction.atomic
def update_item(item):
    return Movie.objects.update_or_create(
        imdb_id=item.imdb_id, defaults=item_to_updated_fields(item))


def get_all_movie_items():
    filename = get_latest_filename()
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        reader = csv.DictReader(f, delimiter='\t')
        yield from map(OMDbItem, reader)


def get_latest_filename():
    all_entries = (
        os.path.join(settings.OMDB_DATA_DIR, filename)
        for filename in os.listdir(settings.OMDB_DATA_DIR))
    non_hidden = filter(lambda x: not x.startswith('.'), all_entries)
    only_directories = filter(os.path.isdir, non_hidden)
    newest_entry = max(only_directories, key=os.path.getctime)
    return os.path.join(newest_entry, 'omdb.txt')


def item_to_updated_fields(item):
    return {
        'title': item.title,
        'year': item.year,
        'mpaa_rating': item.rating,
        'release_date': item.released,
        'imdb_rating': item.imdb_rating,
        'imdb_votes': item.imdb_votes,
        'last_data_update': item.last_updated,
        'last_rating_update': item.last_updated,
    }


class OMDbItem:
    def __init__(self, data):
        self.data = data

    @cached_property
    def title(self):
        return self.data['Title']

    @cached_property
    def year(self):
        return int(self.data['Year'])

    @cached_property
    def rating(self):
        return self.get('Rating', '')

    @cached_property
    def released(self):
        return self.get_date('Released')

    # imdb data

    @cached_property
    def imdb_id(self):
        return self.data['imdbID']

    @cached_property
    def imdb_rating(self):
        return float(self.get('imdbRating', 0.0))

    @cached_property
    def imdb_votes(self):
        string = self.get('imdbVotes', '0')
        digits = ''.join(filter(str.isdigit, string))
        return int(digits)

    # omdb-specific data

    @cached_property
    def last_updated(self):
        return self.get_date('lastUpdated')

    # helpers

    def get_date(self, key, default=None):
        value = self.get(key)
        if value:
            return dateutil.parser.parse(value)
        else:
            return default

    def get(self, key, default=None):
        value = self.data.get(key, default)
        if value == 'N/A':
            return default
        else:
            return value
