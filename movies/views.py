import omdb
from operator import attrgetter
from funcy import group_by

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Movie


class MovieView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/item.html'


class GoView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        imdb_id = self.request.GET.get('imdb_id')
        if not imdb_id:
            return '/'

        year = self.request.GET.get('year')
        title = self.request.GET.get('title')

        movie, created = Movie.objects.get_or_create(imdb_id=imdb_id, defaults={
            'year': year,
            'title': title
        })
        return movie.get_absolute_url()


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'movies/search.html'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return None

        response = omdb.request(s=query, type='movie')
        results = omdb.models.Search(response.json())

        imdb_ids = map(attrgetter('imdb_id'), results)
        movies_in_db = Movie.objects.filter(imdb_id__in=imdb_ids)
        movies_by_imdb_id = group_by(attrgetter('imdb_id'), movies_in_db)
        movies = map(
            lambda result: (movies_by_imdb_id[result.imdb_id][0]
                            if result.imdb_id in movies_by_imdb_id
                            else self.create_movie_from_omdb_result(result)),
            results)

        return list(movies)

    def create_movie_from_omdb_result(self, result):
        movie, created = Movie.objects.get_or_create(
            imdb_id=result.imdb_id, defaults={
                'title': result.title,
                'year': result.year,
            })
        return movie
