import logging
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


def update():
    logger.info("Beginning update")
    total = 0
    for chunk in chunks(1000, get_movie_titles()):
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


def get_movie_titles():
    for item in get_movie_items():
        imdb_id = item.properties[P_IMDB_ID][0]
        for language, title in item.labels.items():
            yield imdb_id, language, title


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
