from django_assets import Bundle, register

from webassets.filter import register_filter
from webassets_browserify import Browserify

register_filter(Browserify)


bundle = Bundle('js/index.js', filters='browserify', output='bundle.js',
                depends='js/**/*.js')

register('bundle', bundle)
