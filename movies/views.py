from operator import attrgetter

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import get_language

from haystack.query import SearchQuerySet

from .models import Movie


class MovieView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/item.html'


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'movies/search.html'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return None

        results = self.get_search_results(query)
        imdb_ids = map(attrgetter('imdb_id'), results)
        movies = Movie.objects.filter(imdb_id__in=imdb_ids)
        movies_by_imdb_id = {m.imdb_id: m for m in movies}
        return [movies_by_imdb_id[result.imdb_id] for result in results]

    def get_search_results(self, query):
        language = get_language()
        translated_param = {'title_%s' % language: query}
        results = (
            SearchQuerySet()
            .filter_or(text=query)
            .filter_or(**translated_param))
        return results[:20]
