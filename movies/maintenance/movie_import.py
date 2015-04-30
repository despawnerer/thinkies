import logging

from sources import omdb

from ..models import Movie


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    total = 0
    for item in omdb.load_latest():
        if item.type == 'movie':
            update_item(item)
            total += 1
            if total % 1000 == 0:
                logger.info("Updated %d movies" % total)
    logger.info("Updated %d movies" % total)
    logger.info("Finished")


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
