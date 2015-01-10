import omdb
from operator import attrgetter
from funcy import group_by

from django.views.generic.list import ListView

from .models import Movie


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'movies/search.html'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return None

        results = omdb.search(query)
        imdb_ids = map(attrgetter('imdb_id'), results)
        movies_in_db = Movie.objects.filter(imdb_id__in=imdb_ids)
        movies_by_imdb_id = group_by(attrgetter('imdb_id'), movies_in_db)
        movies = map(
            lambda result: (movies_by_imdb_id[result.imdb_id]
                            if result.imdb_id in movies_by_imdb_id
                            else self.build_movie_from_omdb_result(result)),
            results)

        return list(movies)

    def build_movie_from_omdb_result(self, result):
        return Movie(title=result.title, imdb_id=result.imdb_id,
                     year=result.year)
