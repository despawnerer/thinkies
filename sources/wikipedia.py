import bz2
import logging
import os
import posixpath
import feedparser
import dateutil.parser
from lxml import etree
from urllib.parse import urlparse
from functools import lru_cache

from pymongo import MongoClient

from django.conf import settings

from .utils import download


logger = logging.getLogger(__name__)


client = MongoClient(
    host=getattr(settings, 'WIKIPEDIA_MONGO_HOST', None),
    port=getattr(settings, 'WIKIPEDIA_MONGO_PORT', None))
db = client[settings.WIKIPEDIA_MONGO_DATABASE]


@lru_cache()
def get_collection(language):
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
    logger.info("Downloading latest %swiki dump..." % language)

    url = get_latest_dump_url(language)
    parsed_url = urlparse(url)
    path, filename = posixpath.split(parsed_url.path)

    local_file_path = os.path.join(settings.WIKIPEDIA_DATA_DIR, filename)
    if os.path.isfile(local_file_path):
        logger.info('Already at the latest version.')
    else:
        download(url, local_file_path)

    return local_file_path


def get_latest_dump_url(language):
    rss_url = ('https://dumps.wikimedia.org/{0}wiki/latest/'
               '{0}wiki-latest-pages-articles.xml.bz2-rss.xml').format(language)
    d = feedparser.parse(rss_url)
    # this is all kind of a error-prone way to get the latest url,
    # but it works for now so eh. FIXME some time.
    dump_path = d.entries[0].link
    dump_date = dump_path[-8:]
    return '{}/{}wiki-{}-pages-articles.xml.bz2'.format(
        dump_path, language, dump_date)


# parsing dumps

def load_dump(filename):
    with bz2.open(filename, 'r') as f:
        yield from parse_dump(f)


def parse_dump(f):
    for page_element in _yield_xml_elements(f, 'page'):
        revision_element = page_element.find('{*}revision')
        yield {
            'title': page_element.find('{*}title').text,
            'id': page_element.find('{*}id').text,
            'revision': {
                'text': revision_element.find('{*}text').text,
                'timestamp': dateutil.parser.parse(
                    revision_element.find('{*}timestamp').text),
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
