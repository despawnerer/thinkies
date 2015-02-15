from haystack.query import SearchQuerySet

from .consts import SEARCHABLE_LANGUAGES


def find(query, languages=None):
    sqs = SearchQuerySet().filter_or(text=query)
    for language in (languages or SEARCHABLE_LANGUAGES):
        param_title = {'title_%s' % language: query}
        param_aliases = {'aliases_%s' % language: query}
        sqs = sqs.filter_or(**param_title).filter_or(**param_aliases)
    return sqs
