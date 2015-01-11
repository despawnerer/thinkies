import logging
import re
from funcy import chunks

from django.db import transaction

from ..models import TitleTranslation
from .. import wikidata


logger = logging.getLogger(__name__)


TYPE_ITEM = 'item'

P_INSTANCE_OF = 'P31'
P_IMDB_ID = 'P345'

Q_ID_FILM = 11424
Q_ID_SHORT_FILM = 24862
Q_ID_ANIMATED_FILM = 202866

PROPERTY_VALUE_FILM = {'entity-type': TYPE_ITEM, 'numeric-id': Q_ID_FILM}
PROPERTY_VALUE_SHORT_FILM = {'entity-type': TYPE_ITEM,
                             'numeric-id': Q_ID_SHORT_FILM}
PROPERTY_VALUE_ANIMATED_FILM = {'entity-type': TYPE_ITEM,
                                'numeric-id': Q_ID_ANIMATED_FILM}


clean_title_re = re.compile(
    r' \((?:'
    r'(?:film|фильм)'
    r'|'
    r'(?:\d{4}.{0,2}(?:film|фильм))'
    r'|'
    r'(?:(?:film|фильм).{0,2}\d{4})'
    r')\)$')


def update():
    logger.info("Beginning update")
    total = 0
    for chunk in chunks(1000, get_all_movie_titles()):
        with transaction.atomic():
            for imdb_id, language, title in chunk:
                TitleTranslation.objects.update_or_create(
                    movie_id=imdb_id,
                    language=language, defaults={
                        'title': title[:255]
                    })
                total += 1
        logger.info("Updated %d titles" % total)
    logger.info("Finished")


def get_all_movie_titles():
    for item in get_movie_items():
        imdb_id = item.properties[P_IMDB_ID][0]
        for language, title in get_movie_titles_from_item(item):
            yield imdb_id, language, title


def get_movie_titles_from_item(item):
    for language, title in item.labels.items():
        yield language, clean_title(title)

    # even if there are no properly translated titles for this movie,
    # there might still be an appropriately-titled wiki page
    for site, title in item.sitelinks.items():
        if not site.endswith('wiki'):
            continue

        language = site[:-4]
        if language in item.labels:
            continue

        yield language, clean_title(title)


def clean_title(title):
    title = title.strip()
    match = clean_title_re.search(title)
    if match:
        title = title[:match.start()] + title[match.end():]
    return title.strip()


def get_movie_items():
    collection = wikidata.get_collection()

    results = collection.find({
        'claims.P31.mainsnak.datavalue.value': {'$in': [
            PROPERTY_VALUE_FILM, PROPERTY_VALUE_SHORT_FILM,
            PROPERTY_VALUE_ANIMATED_FILM]},
        'claims.P345.mainsnak.datavalue.value': {'$exists': True},
    }, fields=['labels', 'claims.P345.mainsnak.datavalue'])

    logger.info("Total movie items: %d", results.count())

    return map(wikidata.Item, results)
