from __future__ import absolute_import, unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import translation
from django.conf import settings

from webassets.ext.jinja2 import AssetsExtension
from django_assets.env import get_env as get_assets_env
from jinja2 import Environment

from users.actions import get_auth_providers


def environment(**options):
    env = Environment(extensions=[AssetsExtension], **options)
    env.assets_environment = get_assets_env()
    env.globals.update({
        'settings': settings,
        'static': staticfiles_storage.url,
        'url': url,

        'get_language': translation.get_language,
        '_': translation.ugettext,

        'get_auth_providers': get_auth_providers,
    })
    return env


def url(view_name, *args, **kwargs):
    return reverse(view_name, args=args, kwargs=kwargs)
