import logging
import re
from funcy import concat
from itertools import product

from django.db import transaction

from thinkies.utils import get_md5, detect_language

from sources import wikidata, wikipedia

from ..consts import SEARCHABLE_LANGUAGES
from ..models import Localization, Poster


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

FILE_PAGE_TITLE_FORMATS = {
    'en': 'File:%s',
    'ru': 'Файл:%s',
}


# TODO: support more languages here
clean_title_re = re.compile(
    r' \((?:'
    r'(?:film|фильм|мультфильм|аниме)'
    r'|'
    r'(?:\d{4}.+(?:film|фильм|мультфильм|аниме))'
    r'|'
    r'(?:(?:film|фильм|мультфильм|аниме).{0,2}\d{4})'
    r')\)$')

filename_re = re.compile(r'[=:]\s*(.+\.(?:jpg|png))')


# overall process

def update():
    logger.info("Beginning update")
    n = 0
    for n, item in enumerate(get_movie_items()):
        update_item(item)
        if n > 0 and n % 1000 == 0:
            logger.info("Updated localizations for %d movies" % n)
    logger.info("Updated localizations for %d movies" % n)
    logger.info("Finished")


def get_movie_items():
    collection = wikidata.get_collection()

    results = collection.find({
        'claims.P31.mainsnak.datavalue.value': {'$in': FILM_TYPE_REFERENCES},
        'claims.P345.mainsnak.datavalue.value': {'$exists': True},
    }, fields=[
        'labels', 'descriptions', 'aliases', 'sitelinks',
        'claims.P345.mainsnak.datavalue'
    ], timeout=False)

    return map(wikidata.Item, results)


# actual updating code

def update_item(item):
    imdb_id_list = item.properties[P_IMDB_ID]
    language_list = get_languages(item)
    for imdb_id, language in product(imdb_id_list, language_list):
        update_item_localization(item, imdb_id, language)

    if len(imdb_id_list) > 1:
        logger.warning("Multiple IMDb ids for single item: %s"
                       % ', '.join(imdb_id_list))


@transaction.atomic
def update_item_localization(item, imdb_id, language):
    localization, created = Localization.objects.update_or_create(
        movie_id=imdb_id, language=language,
        defaults=get_localization_data(item, language))

    poster_source = get_poster_source(localization.wikipedia_page, language)
    if poster_source:
        poster_url, poster_updated = poster_source
        poster = localization.poster or Poster()
        if (poster.source_url != poster_url or
                poster.source_updated != poster_updated):
            poster.source_url = poster_url
            poster.source_updated = poster_updated
            poster.save()

        if not localization.poster:
            localization.poster = poster
            localization.save(update_fields=['poster'])
    else:
        Poster.objects.filter(localization=localization).delete()


def get_languages(item):
    return set(
        language for language in concat(
            [site[:-4] for site in item.sitelinks if site.endswith('wiki')],
            item.labels.keys(),
            item.descriptions.keys(),
        ) if language in SEARCHABLE_LANGUAGES
    )


def get_localization_data(item, language):
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

    wikipedia_page_language = detect_language(wikipedia_page)
    label_language = detect_language(label)

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


def get_poster_source(page_title, language):
    """
    Find the poster on the given wikipedia page.
    Return a tuple of (url, last_update_timestamp)
    """
    # TODO: log errors
    collection = wikipedia.get_collection(language)

    movie_page = collection.find_one({'title': page_title})
    if not movie_page:
        return None

    filename = _find_poster_filename(movie_page)
    if not filename:
        return None

    # get the time of the last update of the file
    file_page_title = FILE_PAGE_TITLE_FORMATS.get(
        language, 'File:%s') % filename
    file_page = collection.find_one({'title': file_page_title})
    if not file_page:
        return None
    file_updated = file_page.get('revision', {}).get('timestamp')

    # generate the filename
    sane_filename = filename.replace(' ', '_')
    hashed_filename = get_md5(sane_filename)
    file_url = 'https://upload.wikimedia.org/wikipedia/{0}/{1}/{2}/{3}'.format(
        language, hashed_filename[0], hashed_filename[:2], sane_filename)

    return file_url, file_updated


def _find_poster_filename(page):
    """
    Find the poster's filename on the page
    The intuition here is that it's probably gonna be the first image
    """
    text = page.get('revision', {}).get('text', '')
    match = filename_re.search(text)
    if match:
        return match.group(1)
    else:
        return None
