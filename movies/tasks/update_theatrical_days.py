import logging
from datetime import date, timedelta
from celery import Task

from django.db.utils import IntegrityError

from sources.google_movies import GoogleMovies

from ..models import TheatricalDay, ParsedMovie
from ..consts import THEATRICAL_RUN_LOCATIONS


logger = logging.getLogger(__name__)


class UpdateTheatricalDaysTask(Task):
    name = 'movies.tasks.update_theatrical_days'

    def run(self):
        for country, city in THEATRICAL_RUN_LOCATIONS:
            for day_offset in range(0, 3):
                self.update_location_for_day_offset(country, city, day_offset)

    def update_location_for_day_offset(self, country, city, day_offset):
        # TODO: take timezones in consideration
        location = '{}, {}'.format(country, city)
        this_date = date.today() + timedelta(days=day_offset)
        grabber = GoogleMovies(location, day_offset)
        item_list = grabber.get_movies()
        for item in item_list:
            if item.imdb_id:
                self.create_theatrical_day(
                    item.imdb_id, country, city, this_date)
            else:
                theaters = grabber.get_theaters_for_movie(item)
                parsed_movie, created = ParsedMovie.objects.get_or_create(
                    source_id=item.mid, defaults={
                        'title': item.title,
                        'additional_data': ', '.join(theaters)
                    })
                if parsed_movie.movie_id:
                    self.create_theatrical_day(
                        parsed_movie.movie_id, country, city, this_date)
        logger.info("Updated {} for {}".format(location, this_date))

    def create_theatrical_day(self, imdb_id, country, city, date):
        try:
            TheatricalDay.objects.create(
                movie_id=imdb_id, country=country, city=city, date=date)
        except IntegrityError:
            pass
