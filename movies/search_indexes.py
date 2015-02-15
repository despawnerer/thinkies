from functools import partial

from haystack import indexes

from thinkies.search.fields import CharField

from .models import Movie
from .consts import (
    SEARCHABLE_LANGUAGES,
    SEARCH_EXACT_TITLE_MATCH_BOOST,
    SEARCH_LANGUAGE_ANALYZERS,
)


class BaseMovieIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='title')
    imdb_id = indexes.CharField(model_attr='imdb_id')
    year = indexes.IntegerField(model_attr='year')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        return self.get_model().objects.prefetch_related('localizations')


def prepare_title(language, obj):
    localization = obj.localizations_by_language.get(language)
    return localization.title if localization else ''


def prepare_aliases(language, obj):
    localization = obj.localizations_by_language.get(language)
    if localization is None:
        return ''

    all_titles = []
    if localization.title:
        all_titles.append(localization.title)

    if localization.aliases:
        all_titles += localization.aliases

    return '\n'.join(all_titles)


index_dict = {}
for language in SEARCHABLE_LANGUAGES:
    analyzer = SEARCH_LANGUAGE_ANALYZERS.get(language)
    index_dict.update({
        'title_%s' % language: CharField(boost=SEARCH_EXACT_TITLE_MATCH_BOOST),
        'aliases_%s' % language: CharField(analyzer=analyzer),
        'prepare_title_%s' % language: partial(prepare_title, language),
        'prepare_aliases_%s' % language: partial(prepare_aliases, language),
    })

MovieIndex = type('MovieIndex', (BaseMovieIndex, indexes.Indexable), index_dict)
