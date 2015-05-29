import bz2
import logging
from lxml import etree

from pymongo import MongoClient

from django.conf import settings


logger = logging.getLogger(__name__)


def get_collection(language):
    client = MongoClient(
        host=getattr(settings, 'WIKIPEDIA_MONGO_HOST', None),
        port=getattr(settings, 'WIKIPEDIA_MONGO_PORT', None))
    db = client[settings.WIKIPEDIA_MONGO_DATABASE]
    collection = db['%swiki' % language]
    collection.ensure_index('id', unique=True)
    collection.ensure_index('title', unique=True)
    return collection


# updating

def update_all():
    logger.info("Updating wiki articles for all languages")
    for language, title in settings.LANGUAGES:
        update(language)


def update(language):
    logger.info("Updating %swiki..." % language)
    filename = download_latest_dump(language)
    update_from_file(language, filename)


def update_from_file(language, filename):
    wiki_name = '%swiki' % language
    logger.info("Loading %s articles..." % wiki_name)

    collection = get_collection(language)
    for n, item in enumerate(load_dump(filename)):
        query = {'id': item['id']}
        collection.update(query, item, upsert=True)
        if n > 0 and n % 1000 == 0:
            logger.info("Loaded %d %s articles" % (n, wiki_name))

    logger.info("Loaded total %d %s articles" % (n, wiki_name))


def download_latest_dump(language):
    logger.info("Downloading latest %swiki dump...")
    raise NotImplementedError


# parsing dumps

def load_dump(filename):
    with bz2.open(filename, 'r') as f:
        yield from parse_dump(f)


def parse_dump(f):
    for page_element in _yield_xml_elements(f, 'page'):
        yield {
            'title': page_element.find('{*}title').text,
            'id': page_element.find('{*}id').text,
            'revision': {
                'text': page_element.find('{*}revision').find('{*}text').text
            }
        }


def _yield_xml_elements(f, tag_name):
    context = etree.iterparse(f, events=('end',))
    context = iter(context)

    for event, elem in context:
        element_tag = _get_namespaceless_element_tag(elem)
        if element_tag == tag_name:
            yield elem
            elem.clear()


def _get_namespaceless_element_tag(element):
    tag = element.tag
    if '}' in tag:
        tag = tag.split('}', 1)[1]
    return tag
