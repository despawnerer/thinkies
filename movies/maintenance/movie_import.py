import logging
from funcy import chunks

from django.db import transaction

from sources import omdb

from ..models import Movie


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    total = 0
    for chunk in chunks(1000, omdb.load_latest()):
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
