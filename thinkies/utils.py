import hashlib
from urllib.request import urlopen
from langdetect import detect as _detect_language
from langdetect.lang_detect_exception import LangDetectException

from django.core.files.base import ContentFile


def get_hashed_file_upload_path(model_instance, filename):
    hashed_filename = get_md5(filename)
    return '{0}/{1}/{2}'.format(
        hashed_filename[0],
        hashed_filename[:2],
        filename)


def load_url(url, name):
    if url is None:
        return None

    # TODO: error handling
    url_content = urlopen(url)
    type_ = url_content.headers.get_content_subtype()
    full_name = '{}.{}'.format(name, type_)
    return ContentFile(url_content.read(), full_name)


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def detect_language(s):
    try:
        return _detect_language(s)
    except LangDetectException:
        return None
