from django.test import TestCase
from django.core.exceptions import ValidationError

from thinkies.validators import validate_imdb_url


class ImdbURLValidatorTestCase(TestCase):
    def test_proper_urls(self):
        validate_imdb_url('http://imdb.com/title/tt3179568')
        validate_imdb_url('http://imdb.com/title/tt3179568/')
        validate_imdb_url('http://www.imdb.com/title/tt3179568')
        validate_imdb_url('http://www.imdb.com/title/tt3179568/')

    def test_wrong_url(self):
        with self.assertRaises(ValidationError):
            validate_imdb_url('http://google.com/')

    def test_imdb_details_url(self):
        with self.assertRaises(ValidationError):
            validate_imdb_url(
                'http://www.imdb.com/title/tt3179568/fullcredits')

    def test_non_title_url(self):
        with self.assertRaises(ValidationError):
            validate_imdb_url('http://www.imdb.com/showtimes')
