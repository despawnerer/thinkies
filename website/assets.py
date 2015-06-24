from django_assets import Bundle, register

from webassets.filter import register_filter
from webassets_browserify import Browserify

from .webassets_postcss import PostCSS


register_filter(Browserify)
register_filter(PostCSS)


register('main_js', Bundle(
    'js/index.js',
    filters='browserify',
    output='gen/bundle.js',
    depends='js/**/*.js'))


register('main_css', Bundle(
    'css/index.css',
    filters='postcss',
    output='gen/bundle.css',
    depends='css/**/*.css'))
