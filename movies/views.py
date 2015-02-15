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


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'movies/search.html'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return None

        friends = get_friends(self.request.user)

        results = self.get_search_results(query)
        imdb_ids = map(attrgetter('imdb_id'), results)
        prefetch_localizations = Prefetch(
            'localizations',
            queryset=Localization.objects.filter(language=get_language()))
        prefetch_opinions = Prefetch(
            'opinions', to_attr='friend_opinions',
            queryset=Opinion.objects.filter(author__in=friends))
        movies = (
            Movie.objects
            .filter(imdb_id__in=imdb_ids)
            .prefetch_related(prefetch_localizations, prefetch_opinions))
        movies_by_imdb_id = {m.imdb_id: m for m in movies}
        return [movies_by_imdb_id[result.imdb_id] for result in results]

    def get_search_results(self, query):
        current_language = get_language()

        languages = [current_language]
        try:
            detected_language = detect_language(query)
            if (detected_language in SEARCHABLE_LANGUAGES
                    and detected_language != current_language):
                languages.append(detected_language)
        except LangDetectException:
            # TODO: log these?
            pass

        return search.find(query, languages)[:20]


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
