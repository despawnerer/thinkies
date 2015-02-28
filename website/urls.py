from django.conf.urls import url

from .views.index import Index
from .views.search import SearchView
from .views.movie import MovieView


urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^movies/(?P<pk>\d+)/$', MovieView.as_view(), name='movie'),
]
