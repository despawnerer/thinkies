from urllib.request import urlopen

from django.core.files.base import ContentFile


def load_url(url, name):
    if url is None:
        return None

    # TODO: error handling
    url_content = urlopen(url)
    type_ = url_content.headers.get_content_subtype()
    full_name = '{}.{}'.format(name, type_)
    return ContentFile(url_content.read(), full_name)
