"""
Django settings for thoughts project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8#o_-qrj3k8w^-2ww81u$+w7zu6@3re#r$(q=$3t=@clo54)ev'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'haystack',
    'social.apps.django_app.default',

    'thoughts',
    'movies',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
)

ROOT_URLCONF = 'thoughts.urls'

WSGI_APPLICATION = 'thoughts.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thoughts',
        'USER': 'thoughts',
        'PASSWORD': 'thisreallydoesntmatter',
        'HOST': ''
    }
}


AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
)

SOCIAL_AUTH_TWITTER_KEY = 'ByaSI7W75mLRTcWCjd5gHRn7O'
SOCIAL_AUTH_TWITTER_SECRET = '0gZSlM7c8sYa0zZx3upgbf1wYraQyQpqLxPEPY5b3cdLTvkn3T'


LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


GEOIP_PATH = os.path.join(DATA_DIR, 'geoip')
GEOIP_CITY = 'GeoLite2-City.mmdb'

WIKIDATA_DIR = os.path.join(DATA_DIR, 'wikidata')


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'thoughts.search.engines.ConfigurableElasticEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'thoughts',
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'movies.maintenance': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
