from operator import attrgetter
from langdetect import detect as detect_language
from langdetect.lang_detect_exception import LangDetectException

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import get_language
from django.db.models import Prefetch

from haystack.query import SearchQuerySet

from .models import Movie, TitleTranslation
from .consts import SEARCHABLE_LANGUAGES


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
        prefetch = Prefetch(
            'title_translations',
            queryset=TitleTranslation.objects.filter(language=get_language()))
        movies = (
            Movie.objects
            .filter(imdb_id__in=imdb_ids)
            .prefetch_related(prefetch))
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
