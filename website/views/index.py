from datetime import timedelta

from django.views.generic import ListView
from django.utils import timezone
from django.utils.translation import get_language
from django.db.models import Prefetch

from users.actions import get_friends

from opinions.models import Tip

from movies.models import Localization, Movie
from movies.consts import THEATRICAL_RUN_LOCATIONS


class Index(ListView):
    template_name = 'pages/index.jinja2'
    context_object_name = 'movie_list'

    def get_queryset(self):
        friends = get_friends(self.request.user)
        prefetch_localizations = Prefetch(
            'localizations',
            queryset=Localization.objects.filter(language=get_language()))
        prefetch_tips = Prefetch(
            'tips', to_attr='friend_tips',
            queryset=Tip.objects.filter(author__in=friends))

        if self.request.location:
            qs = self.get_queryset_for_location(self.request.location)
        else:
            qs = self.get_generic_queryset()

        return qs.prefetch_related(
            prefetch_localizations, prefetch_tips)[:50]

    def get_queryset_for_location(self, location):
        country, city = location
        if (country, city) in THEATRICAL_RUN_LOCATIONS:
            return self.get_queryset_in_theaters_in_city(country, city)
        return self.get_generic_queryset()

    def get_queryset_in_theaters_in_city(self, country, city):
        today = timezone.now().today()
        return (
            Movie.objects
            .filter(theatrical_days__country=country,
                    theatrical_days__city=city,
                    theatrical_days__date=today)
            .order_by('-imdb_votes'))

    def get_generic_queryset(self):
        now = timezone.now()
        three_months_ago = now - timedelta(days=90)
        return (
            Movie.objects
            .filter(release_date__lt=now, release_date__gt=three_months_ago)
            .order_by('-imdb_votes'))
