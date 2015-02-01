from operator import attrgetter
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException
from itertools import chain

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import get_language
from django.db.models import Prefetch

from haystack.query import SearchQuerySet

from users.actions import get_friends
from tips.models import Tip

from .models import Movie, TitleTranslation, ParsedMovie
from .consts import SEARCHABLE_LANGUAGES


class MovieView(DetailView):
    model = Movie
    template_name = 'movies/item.html'

    def get_context_data(self, **kwargs):
        context = {
            'movie': self.object,
            'tip_list': self.get_tips(),
        }
        context.update(kwargs)
        return context

    def get_tips(self):
        all_tips = self.object.tips.all()
        user = self.request.user
        if not user.is_authenticated():
            return all_tips

        friends = get_friends(user)
        friend_tips = all_tips.filter(author__in=friends)
        other_tips = all_tips.exclude(author__in=friends)
        return chain(friend_tips, other_tips)


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'movies/search.html'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return None

        if self.request.user.is_authenticated():
            friends = get_friends(self.request.user)
        else:
            friends = []

        results = self.get_search_results(query)
        imdb_ids = map(attrgetter('imdb_id'), results)
        prefetch_titles = Prefetch(
            'title_translations',
            queryset=TitleTranslation.objects.filter(language=get_language()))
        prefetch_tips = Prefetch(
            'tips', to_attr='friend_tips',
            queryset=Tip.objects.filter(author__in=friends))
        movies = (
            Movie.objects
            .filter(imdb_id__in=imdb_ids)
            .prefetch_related(prefetch_titles, prefetch_tips))
        movies_by_imdb_id = {m.imdb_id: m for m in movies}
        return [movies_by_imdb_id[result.imdb_id] for result in results]

    def get_search_results(self, query):
        language_set = {get_language()}

        try:
            language_set.add(detect_language(query))
        except LangDetectException:
            # TODO: log these?
            pass

        sqs = SearchQuerySet().filter_or(text=query)
        for language in language_set:
            if language in SEARCHABLE_LANGUAGES:
                param = {'title_%s' % language: query}
                sqs = sqs.filter_or(**param)
        return sqs[:20]


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
        sqs = SearchQuerySet().filter_or(text=query)
        for language in SEARCHABLE_LANGUAGES:
            param = {'title_%s' % language: query}
            sqs = sqs.filter_or(**param)

        try:
            result = sqs[0]
            return Movie.objects.get(imdb_id=result.imdb_id)
        except IndexError:
            return None

    def sanitize_title(self, title):
        if title.endswith(' 3D'):
            return title[:-4]
        return title
