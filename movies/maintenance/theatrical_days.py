import logging
from datetime import date, timedelta

from django.db.utils import IntegrityError

from sources.google_movies import GoogleMovies

from ..models import TheatricalDay, ParsedMovie
from ..consts import THEATRICAL_RUN_LOCATIONS


logger = logging.getLogger(__name__)


def update():
    logger.info("Beginning update")
    today = date.today()
    for country, city in THEATRICAL_RUN_LOCATIONS:
        location = '{}, {}'.format(country, city)
        for day_offset in range(0, 3):
            # TODO: take timezones in consideration
            this_date = today + timedelta(days=day_offset)
            grabber = GoogleMovies(location, day_offset)
            item_list = grabber.get_movies()
            for item in item_list:
                if item.imdb_id:
                    create_theatrical_day(
                        item.imdb_id, country, city, this_date)
                else:
                    parsed_movie, created = ParsedMovie.objects.get_or_create(
                        source_id=item.mid, defaults={'title': item.title})
                    if parsed_movie.movie_id:
                        create_theatrical_day(
                            parsed_movie.movie_id, country, city, this_date)
            logger.info("Updated {} for {}".format(location, this_date))
    logger.info("Finished")


def create_theatrical_day(imdb_id, country, city, date):
    try:
        TheatricalDay.objects.create(movie_id=imdb_id, country=country,
                                     city=city, date=date)
    except IntegrityError:
        pass
