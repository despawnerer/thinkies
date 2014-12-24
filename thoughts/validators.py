from urllib.parse import urlsplit

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_imdb_url(value):
    scheme, netloc, path, query, fragment = urlsplit(value)
    split_path = path.strip('/').split('/')

    is_fine = (
        netloc in ('imdb.com', 'www.imdb.com')
        and query == ''
        and len(split_path) == 2
        and split_path[0] == 'title'
        and split_path[1].startswith('tt'))

    if not is_fine:
        raise ValidationError(_("Please enter a correct URL"))
