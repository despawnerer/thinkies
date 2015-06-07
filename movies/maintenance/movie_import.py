import logging

from django.db import transaction
from django.utils.timezone import now

from sources import omdb

from ..models import Movie, Poster


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    for n, item in enumerate(omdb.load_latest()):
        if item.type == 'movie':
            update_item(item)
            if n % 1000 == 0:
                logger.info("Updated %d movies" % n)
    logger.info("Updated %d movies" % n)
    logger.info("Finished")


@transaction.atomic
def update_item(item):
    movie, created = Movie.objects.update_or_create(
        imdb_id=item.imdb_id, defaults=item_to_updated_fields(item))

    if item.poster:
        poster = movie.poster or Poster()
        if poster.source_url != item.poster:
            poster.source_url = item.poster
            poster.source_updated = now()
            poster.save()

        if not movie.poster:
            movie.poster = poster
            movie.save(update_fields=['poster'])
    else:
        Poster.objects.filter(movie=movie).delete()


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
