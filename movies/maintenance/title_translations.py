import os
import gzip
import logging
import glob
from funcy import chunks

from django.conf import settings
from django.db import transaction

from ..models import TitleTranslation
from .. import wikidata


logger = logging.getLogger(__name__)


ITEM_TYPE = 'item'

P_INSTANCE_OF = 'P31'
P_IMDB_ID = 'P345'

Q_ID_FILM = 11424

PROPERTY_VALUE_FILM = {'entity-type': ITEM_TYPE, 'numeric-id': Q_ID_FILM}


def update():
    filename = get_latest_archive_filename()
    io = get_io_for_filename(filename)
    f = io(filename, 'rb')

    logger.info("Beginning update from %s" % filename)
    total = 0
    for chunk in chunks(100, get_movie_titles(f)):
        with transaction.atomic():
            for imdb_id, language, title in chunk:
                TitleTranslation.objects.update_or_create(
                    movie_id=imdb_id,
                    language=language, defaults={
                        'title': title
                    })
                total += 1
        logger.info("Updated %d titles" % total)
    f.close()
    logger.info("Finished")


def get_latest_archive_filename():
    pattern = os.path.join(settings.WIKIDATA_DIR, '*.json.gz')
    latest_filename = max(glob.iglob(pattern), key=os.path.getctime)
    return latest_filename


def get_io_for_filename(filename):
    if filename.endswith('.json.gz'):
        return gzip.open
    elif filename.endswith('.json'):
        return open
    else:
        raise RuntimeError("Wikidata archive file isn't json. What?")


def get_movie_titles(f):
    all_items = wikidata.load_items(f)
    movie_items = filter(is_item_movie, all_items)
    for item in movie_items:
        imdb_id = item.properties[P_IMDB_ID][0]
        for language, title in item.labels.items():
            yield imdb_id, language, title


def is_item_movie(item):
    return (
        item.type == ITEM_TYPE
        and P_INSTANCE_OF in item.properties
        and P_IMDB_ID in item.properties
        and PROPERTY_VALUE_FILM in item.properties[P_INSTANCE_OF])
