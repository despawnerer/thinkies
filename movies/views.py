from operator import attrgetter
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException
from itertools import chain

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import get_language
from django.db.models import Prefetch

from users.actions import get_friends
from opinions.models import Opinion

from .models import Movie, Localization, ParsedMovie
from .consts import SEARCHABLE_LANGUAGES
from . import search


class MovieView(DetailView):
    model = Movie
    template_name = 'movies/item.html'

    def get_context_data(self, **kwargs):
        context = {
            'movie': self.object,
            'opinion_list': self.get_opinions(),
        }
        context.update(kwargs)
        return context

    def get_opinions(self):
        friends = get_friends(self.request.user)
        all_opinions = self.object.opinions.all()
        friend_opinions = all_opinions.filter(author__in=friends)
        other_opinions = all_opinions.exclude(author__in=friends)
        return chain(friend_opinions, other_opinions)




class ParsedMoviesView(ListView):
    model = ParsedMovie
    template_name = 'movies/parsed_movies.html'
    context_object_name = 'parsed_movie_list'

    def get_queryset(self):
        parsed_movie_list = (
            ParsedMovie.objects
            .select_related('movie')
            .order_by('-id'))

        for parsed_movie in parsed_movie_list:
            if not parsed_movie.is_rejected and not parsed_movie.movie_id:
                query = self.sanitize_title(parsed_movie.title)
                parsed_movie.suggestion = self.get_suggestion(query)

        return parsed_movie_list

    def get_suggestion(self, query):
        search_results = search.find(query)[:1]

        try:
            result = search_results[0]
            return Movie.objects.get(imdb_id=result.imdb_id)
        except IndexError:
            return None

    def sanitize_title(self, title):
        if title.endswith(' 3D'):
            return title[:-4]
        return title
