import logging
import re
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException
from funcy import concat
from itertools import product

from sources import wikidata

from ..models import Localization

from ..consts import SEARCHABLE_LANGUAGES


logger = logging.getLogger(__name__)


TYPE_ITEM = 'item'

P_INSTANCE_OF = 'P31'
P_IMDB_ID = 'P345'

Q_ID_FILM = 11424
Q_ID_SHORT_FILM = 24862
Q_ID_FEATURE_FILM = 24869
Q_ID_DOCUMENTARY_FILM = 93204
Q_ID_TV_FILM = 506240
Q_ID_ANIMATED_FILM = 202866
Q_ID_STOP_MOTION = 18089587

FILM_TYPE_Q_IDS = [Q_ID_FILM, Q_ID_FEATURE_FILM, Q_ID_SHORT_FILM,
                   Q_ID_DOCUMENTARY_FILM, Q_ID_TV_FILM, Q_ID_ANIMATED_FILM,
                   Q_ID_STOP_MOTION]

FILM_TYPE_REFERENCES = [
    {'entity-type': TYPE_ITEM, 'numeric-id': id_}
    for id_ in FILM_TYPE_Q_IDS
]


# TODO: support more languages here
clean_title_re = re.compile(
    r' \((?:'
    r'(?:film|фильм|мультфильм|аниме)'
    r'|'
    r'(?:\d{4}.+(?:film|фильм|мультфильм|аниме))'
    r'|'
    r'(?:(?:film|фильм|мультфильм|аниме).{0,2}\d{4})'
    r')\)$')


def update():
    logger.info("Beginning update")
    total = 0
    for imdb_id, language, localization_data in get_all_localizations():
        Localization.objects.update_or_create(
            movie_id=imdb_id, language=language,
            defaults=localization_data)
        total += 1
        if total % 1000 == 0:
            logger.info("Updated %d localizations" % total)
    logger.info("Updated %d localizations" % total)
    logger.info("Finished")


def get_all_localizations():
    for item in get_movie_items():
        imdb_id_list = item.properties[P_IMDB_ID]
        language_list = get_languages_for_item(item)
        for imdb_id, language in product(imdb_id_list, language_list):
            localization_data = get_localization_data_from_item(item, language)
            yield imdb_id, language, localization_data
        if len(imdb_id_list) > 1:
            logger.warning("Multiple IMDb ids for single item: %s"
                           % ', '.join(imdb_id_list))


def get_languages_for_item(item):
    return set(
        language for language in concat(
            [site[:-4] for site in item.sitelinks if site.endswith('wiki')],
            item.labels.keys(),
            item.descriptions.keys(),
        ) if language in SEARCHABLE_LANGUAGES
    )


def get_localization_data_from_item(item, language):
    wikipedia_page = item.sitelinks.get(language + 'wiki', '')
    label = item.labels.get(language, '')
    description = item.descriptions.get(language, '')
    aliases = item.aliases.get(language, [])
    title = clean_title(choose_title(wikipedia_page, label, language))

    return {
        'wikipedia_page': wikipedia_page,
        'title': title[:255],
        'description': description,
        'aliases': list(map(lambda x: x[:255], aliases)),
    }


def choose_title(wikipedia_page, label, language):
    """
    Choose the likelier proper title of the movie in the given language,
    from the wikipedia page title and the label from wikidata.

    Wikipedia page titles are preferred over wikidata labels
    cause they tend to represent the 'popular' title of the movie
    much better, even though they often need significant cleanup.

    But sometimes, wikipedia page titles are actually in english
    for some reason and wikidata might have the correctly translated
    title, so in cases when we have both, we attempt to detect the
    languages and take the label if it fits but the wiki page title doesn't.
    """

    if not wikipedia_page:
        return label
    elif not label:
        return wikipedia_page

    try:
        wikipedia_page_language = detect_language(wikipedia_page)
        label_language = detect_language(label)
    except LangDetectException:
        return wikipedia_page

    if wikipedia_page_language == label_language:
        return wikipedia_page
    elif label_language == language:
        return label
    else:
        return wikipedia_page


def clean_title(title):
    """
    Remove bullshit qualifiers from the title.

    E.g.:
    My Awesome Movie (2014 American movie) -> My Awesome Movie
    """
    title = title.strip()
    match = clean_title_re.search(title)
    if match:
        title = title[:match.start()] + title[match.end():]
    return title.strip()


def get_movie_items():
    collection = wikidata.get_collection()

    results = collection.find({
        'claims.P31.mainsnak.datavalue.value': {'$in': FILM_TYPE_REFERENCES},
        'claims.P345.mainsnak.datavalue.value': {'$exists': True},
    }, fields=[
        'labels', 'descriptions', 'aliases', 'sitelinks',
        'claims.P345.mainsnak.datavalue'
    ], timeout=False)

    logger.info("Total movie items: %d", results.count())

    return map(wikidata.Item, results)
