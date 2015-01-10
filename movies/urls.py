from django.conf.urls import url

from .views import SearchView, MovieView, GoView


urlpatterns = [
    url(r'^(?P<pk>\d+)/', MovieView.as_view(), name='movie'),
    url(r'^go/', GoView.as_view(), name='go'),
    url(r'^search/', SearchView.as_view(), name='search')
]
