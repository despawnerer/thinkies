import os
import csv
import dateutil.parser
from funcy import cached_property

from django.conf import settings


# loading

def load_latest():
    filename = get_latest_filename()
    yield from load_from_filename(filename)


def load_from_filename(filename):
    with open(filename, 'r', encoding='ISO-8859-1', newline='\r\n') as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE,
                                strict=True)
        yield from map(Item, reader)


def get_latest_filename():
    all_entries = (
        os.path.join(settings.OMDB_DATA_DIR, filename)
        for filename in os.listdir(settings.OMDB_DATA_DIR))
    non_hidden = filter(lambda x: not x.startswith('.'), all_entries)
    only_directories = filter(os.path.isdir, non_hidden)
    newest_directory = max(only_directories, key=os.path.getctime)
    possible_filenames = ('omdb.txt', 'omdbFull.txt', 'omdbMovies.txt')
    for filename in possible_filenames:
        file_path = os.path.join(newest_directory, filename)
        if os.path.isfile(file_path):
            return file_path


# data classes

class Item:
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

    @cached_property
    def type(self):
        return self.data['Type']

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
