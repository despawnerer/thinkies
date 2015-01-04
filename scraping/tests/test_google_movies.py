from unittest import TestCase

from scraping.sources import GoogleMovies
from scraping.utils import first


TOTAL_MOVIES_COUNT_THRESHOLD = 5  # arbitrary
THEATERS_FOR_MOVIE_COUNT_THRESHOLD = 1


class GoogleTestCase(TestCase):
    def test_movies_in_russian_location(self):
        location = 'Saint Petersburg, Russia'
        showtimes = GoogleMovies(location)
        movies = showtimes.get_movies()
        self.assertGreater(len(movies), TOTAL_MOVIES_COUNT_THRESHOLD)

    def test_movies_in_american_location(self):
        location = 'Mountain View'
        showtimes = GoogleMovies(location)
        movies = showtimes.get_movies()
        self.assertGreater(len(movies), TOTAL_MOVIES_COUNT_THRESHOLD)
        movie = first(movies)
        self.assertTrue(bool(movie.imdb_id))

    def test_theaters_for_movie(self):
        location = 'Saint Petersburg, Russia'
        showtimes = GoogleMovies(location)
        movie = first(showtimes.get_movies())
        theaters_for_movie = showtimes.get_theaters_for_movie(movie)
        self.assertGreater(len(theaters_for_movie),
                           THEATERS_FOR_MOVIE_COUNT_THRESHOLD)
