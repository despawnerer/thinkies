import omdb
from operator import attrgetter
from funcy import group_by
from itertools import chain

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

        our_results = self.get_our_results(query)
        our_imdb_ids = set(map(attrgetter('imdb_id'), our_results))

        omdb_results = self.get_omdb_results(query)
        omdb_results = list(filter(
            lambda result: result.imdb_id not in our_imdb_ids, omdb_results))
        omdb_imdb_ids = set(map(attrgetter('imdb_id'), omdb_results))

        imdb_ids = our_imdb_ids | omdb_imdb_ids
        movies_in_db = Movie.objects.filter(imdb_id__in=imdb_ids)
        movies_by_imdb_id = group_by(attrgetter('imdb_id'), movies_in_db)

        our_movies = map(
            lambda result: movies_by_imdb_id[result.imdb_id][0], our_results)
        omdb_movies = map(
            lambda result: (movies_by_imdb_id[result.imdb_id][0]
                            if result.imdb_id in movies_by_imdb_id
                            else self.create_movie_from_omdb_result(result)),
            omdb_results)

        return chain(our_movies, omdb_movies)

    def get_our_results(self, query):
        language = get_language()
        translated_param = {'title_%s' % language: query}
        results = (
            SearchQuerySet()
            .filter_or(text=query)
            .filter_or(**translated_param))
        return results[:20]

    def get_omdb_results(self, query):
        try:
            response = omdb.request(s=query, type='movie')
        except:
            return []

        results = omdb.models.Search(response.json())
        return results

    def create_movie_from_omdb_result(self, result):
        movie, created = Movie.objects.get_or_create(
            imdb_id=result.imdb_id, defaults={
                'title': result.title,
                'year': result.year,
            })
        return movie
