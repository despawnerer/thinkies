import os
import json

from django.test import TestCase

from movies.maintenance.title_translations import (
    get_movie_titles_from_item,
    clean_title,
)

from sources.wikidata import Item


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class GetMovieTitlesForItemTestCase(TestCase):
    def setUp(self):
        filename = 'data/movie_item.json'
        with open(os.path.join(TEST_ROOT, filename)) as f:
            data = json.load(f)
        self.item = Item(data)

    def test_titles_get_picked_up_from_sitelinks(self):
        expected_titles = set([
            ('fr', 'Whiplash'),
            ('en', 'Whiplash'),
            ('it', 'Whiplash'),
            ('ko', '위플래쉬'),
            ('es', 'Whiplash'),
            ('zh-hk', '鼓動真我'),
            ('hr', 'Ritam ludila'),
            ('nl', 'Whiplash'),
            ('zh', '爆裂鼓手'),
            ('fi', 'Whiplash (elokuva)'),  # eh, TODO
            ('ru', 'Одержимость')
        ])
        titles = set(get_movie_titles_from_item(self.item))
        self.assertEqual(expected_titles, titles)


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
