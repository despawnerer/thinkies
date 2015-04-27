from django.conf.urls import url

from .views.index import Index
from .views.search import SearchView
from .views.movie import MovieView
from .views.settings import SettingsView


urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^movies/(?P<pk>\d+)/$', MovieView.as_view(), name='movie'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
]
