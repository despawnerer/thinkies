import logging
import re
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException

from sources import wikidata

from ..models import TitleTranslation


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
    r'(?:film|фильм|мультфильм)'
    r'|'
    r'(?:\d{4}.+(?:film|фильм|мультфильм))'
    r'|'
    r'(?:(?:film|фильм|мультфильм).{0,2}\d{4})'
    r')\)$')


def update():
    logger.info("Beginning update")
    total = 0
    for imdb_id, language, title in get_all_movie_titles():
        TitleTranslation.objects.update_or_create(
            movie_id=imdb_id, language=language,
            defaults={
                'title': title[:255]
            })
        total += 1
        if total % 1000 == 0:
            logger.info("Updated %d titles" % total)
    logger.info("Updated %d titles" % total)
    logger.info("Finished")


def get_all_movie_titles():
    for item in get_movie_items():
        imdb_id = item.properties[P_IMDB_ID][0]
        for language, title in get_movie_titles_from_item(item):
            yield imdb_id, language, title


def get_movie_titles_from_item(item):
    # wikipedia page titles are preferred over wikidata labels
    # cause they tend to represent the 'popular' title of the movie
    # much better, even though they often need significant cleanup
    #
    # but sometimes, wikipedia page titles are actually in english
    # for some reason and wikidata might have the correctly translated
    # title, so in cases when we have both, we attempt to detect the
    # languages and take the label if it fits but the wiki page title doesn't

    wiki_titles = {}
    for site, title in item.sitelinks.items():
        if not site.endswith('wiki'):
            continue
        language = site[:-4]
        wiki_titles[language] = title

    for language, title in wiki_titles.items():
        if language not in item.labels:
            yield language, clean_title(title)
            continue

        label = item.labels[language]
        try:
            detected_title_language = detect_language(title)
            detected_label_language = detect_language(label)
        except LangDetectException:
            yield language, clean_title(title)
            continue

        if detected_title_language == detected_label_language:
            yield language, clean_title(title)
        elif detected_label_language == language:
            yield language, clean_title(label)
        else:
            yield language, clean_title(title)

    for language, label in item.labels.items():
        if language not in wiki_titles:
            yield language, clean_title(label)


def clean_title(title):
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
        'labels', 'sitelinks', 'claims.P345.mainsnak.datavalue'
    ], timeout=False)

    logger.info("Total movie items: %d", results.count())

    return map(wikidata.Item, results)
