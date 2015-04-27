import os

from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NODE_BIN_DIR = os.path.join(BASE_DIR, 'node_modules', '.bin')


SECRET_KEY = '8#o_-qrj3k8w^-2ww81u$+w7zu6@3re#r$(q=$3t=@clo54)ev'


DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'debug_toolbar',
    'haystack',
    'social.apps.django_app.default',
    'rest_framework',
    'django_assets',

    'thinkies',
    'users',
    'movies',
    'opinions',

    'api',
    'website',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'website.middleware.location.LocationMiddleware',
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

ROOT_URLCONF = 'thinkies.urls'

WSGI_APPLICATION = 'thinkies.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thoughts',
        'USER': 'thoughts',
        'PASSWORD': 'thisreallydoesntmatter',
        'HOST': ''
    }
}


AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.Facebook2OAuth2',
    'social.backends.vk.VKOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'users.social_auth.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'users.social_auth.create_identity',
    'users.social_auth.send_signal'
)

SOCIAL_AUTH_TWITTER_KEY = 'ByaSI7W75mLRTcWCjd5gHRn7O'
SOCIAL_AUTH_TWITTER_SECRET = '0gZSlM7c8sYa0zZx3upgbf1wYraQyQpqLxPEPY5b3cdLTvkn3T'

SOCIAL_AUTH_FACEBOOK_KEY = '1623017964587689'
SOCIAL_AUTH_FACEBOOK_SECRET = 'c6d78295fd08aec4bd43692529032291'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['user_friends', 'email', 'public_profile']


LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


BROWSERIFY_BIN = os.path.join(NODE_BIN_DIR, 'browserify')


GEOIP_PATH = os.path.join(DATA_DIR, 'geoip')
GEOIP_CITY = 'GeoLite2-City.mmdb'

WIKIDATA_DIR = os.path.join(DATA_DIR, 'wikidata')
WIKIDATA_MONGO_HOST = 'localhost'
WIKIDATA_MONGO_DATABASE = 'test'

OMDB_DATA_DIR = os.path.join(DATA_DIR, 'omdb')


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'thinkies.search.engines.ConfigurableElasticEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'thinkies',
    },
}


REST_FRAMEWORK = {
    'PAGINATE_BY': 10
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
        'simple_with_time': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple_with_time'
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
