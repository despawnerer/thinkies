import logging
import csv
import os
from funcy import chunks

from django.db import transaction
from django.conf import settings

from ..models import Movie


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    total = 0
    for chunk in chunks(1000, get_all_movie_dicts()):
        with transaction.atomic():
            for movie_dict in chunk:
                imdb_id = movie_dict['imdbID']
                Movie.objects.update_or_create(
                    imdb_id=imdb_id,
                    defaults=movie_dict_to_fields(movie_dict))
                total += 1
        logger.info("Updated %d movies" % total)
    logger.info("Finished")


def get_all_movie_dicts():
    filename = get_latest_filename()
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        reader = csv.DictReader(f, delimiter='\t')
        yield from reader


def get_latest_filename():
    all_entries = (
        os.path.join(settings.OMDB_DATA_DIR, filename)
        for filename in os.listdir(settings.OMDB_DATA_DIR))
    non_hidden = filter(lambda x: not x.startswith('.'), all_entries)
    only_directories = filter(os.path.isdir, non_hidden)
    newest_entry = max(only_directories, key=os.path.getctime)
    return os.path.join(newest_entry, 'omdb.txt')


def movie_dict_to_fields(movie_dict):
    omdb_field_to_our_field = {
        'imdbRating': 'imdb_rating',
        'Title': 'title',
        'Year': 'year',
        'Country': 'country',
    }
    return {our_field: movie_dict[omdb_field]
            for omdb_field, our_field in omdb_field_to_our_field.items()
            if has_actual_value(movie_dict, omdb_field)}


def has_actual_value(movie_dict, key):
    value = movie_dict.get(key)
    if value == 'N/A':
        return False
    else:
        return bool(value)
