from operator import attrgetter

from django.views.generic import ListView
from django.db.models import Prefetch
from django.utils.translation import get_language

from thinkies.utils import detect_language

from movies.models import Movie, Localization
from movies.consts import SEARCHABLE_LANGUAGES
from movies import search

from opinions.models import Tip

from users.actions import get_friends


class SearchView(ListView):
    context_object_name = 'movie_list'
    template_name = 'pages/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q') or ''
        return context

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
        prefetch_tips = Prefetch(
            'tips', to_attr='friend_tips',
            queryset=Tip.objects.filter(author__in=friends))
        movies = (
            Movie.objects
            .filter(imdb_id__in=imdb_ids)
            .prefetch_related(prefetch_localizations, prefetch_tips))
        movies_by_imdb_id = {m.imdb_id: m for m in movies}
        return [movies_by_imdb_id[result.imdb_id] for result in results]

    def get_search_results(self, query):
        current_language = get_language()

        languages = [current_language]
        detected_language = detect_language(query)
        if (detected_language in SEARCHABLE_LANGUAGES
                and detected_language != current_language):
            languages.append(detected_language)

        return search.find(query, languages)[:20]
