import os

from django.test import TestCase

from movies.maintenance.localizations import (
    clean_title,
)


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class CleanTitleTestCase(TestCase):
    def test_english(self):
        original_titles = [
            'Whiplash',
            'Whiplash (film)',
            'Whiplash (2014 film)',
            'Whiplash (2014, film)',
            'Whiplash (film 2014)',
            'Whiplash (film, 2014)',
        ]
        expected_title = 'Whiplash'
        for title in original_titles:
            self.assertEqual(clean_title(title), expected_title)

    def test_english_with_country(self):
        original_title = 'Frozen (2010 American film)'
        expected_title = 'Frozen'
        self.assertEqual(clean_title(original_title), expected_title)

    def test_english_false_negatives(self):
        titles_that_need_no_modification = (
            'Small Medium Large (Fits All Sizes)',
        )
        for title in titles_that_need_no_modification:
            self.assertEqual(clean_title(title), title)

    def test_russian(self):
        original_titles = [
            'Одержимость',
            'Одержимость (фильм)',
            'Одержимость (фильм 2014)',
            'Одержимость (фильм, 2014)',
            'Одержимость (2014 фильм)',
            'Одержимость (2014, фильм)',
        ]
        expected_title = 'Одержимость'
        for title in original_titles:
            self.assertEqual(clean_title(title), expected_title)

    def test_russian_animated(self):
        original_titles = [
            'Пингвины из Мадагаскара',
            'Пингвины из Мадагаскара (мультфильм)',
            'Пингвины из Мадагаскара (мультфильм 2014)',
            'Пингвины из Мадагаскара (мультфильм, 2014)',
            'Пингвины из Мадагаскара (2014 мультфильм)',
            'Пингвины из Мадагаскара (2014, мультфильм)',
        ]
        expected_title = 'Пингвины из Мадагаскара'
        for title in original_titles:
            self.assertEqual(clean_title(title), expected_title)

    def test_russian_anime(self):
        original_titles = [
            'Оборотни',
            'Оборотни (аниме)',
            'Оборотни (аниме 1999)',
            'Оборотни (аниме, 1999)',
            'Оборотни (1999 аниме)',
            'Оборотни (1999, аниме)',
        ]
        expected_title = 'Оборотни'
        for title in original_titles:
            self.assertEqual(clean_title(title), expected_title)
