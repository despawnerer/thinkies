from django.conf.urls import url

from .views import SearchView, MovieView


urlpatterns = [
    url(r'^(?P<pk>\d+)/', MovieView.as_view(), name='movie'),
    url(r'^search/', SearchView.as_view(), name='search')
]
