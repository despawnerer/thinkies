from django.test import TestCase
from django.utils import translation

from .factories import MovieFactory, LocalizationFactory


class TranslatedLensTestCase(TestCase):
    def test_without_localization(self):
        language = 'ru'
        movie = MovieFactory.create(title="Generic Title")
        with translation.override(language):
            self.assertEqual(movie.translated.title, "Generic Title")

    def test_with_localization(self):
        language = 'ru'
        movie = MovieFactory.create(title="Generic Title")
        LocalizationFactory.create(
            language=language, movie=movie, title="Local Title")
        with translation.override(language):
            self.assertEqual(movie.translated.title, "Local Title")

    def test_with_localization_with_no_title(self):
        language = 'ru'
        movie = MovieFactory.create(title="Generic Title")
        LocalizationFactory.create(
            language=language, movie=movie, title="")
        with translation.override(language):
            self.assertEqual(movie.translated.title, "Generic Title")
