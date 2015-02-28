from itertools import chain

from django.views.generic import DetailView

from users.actions import get_friends

from movies.models import Movie


class MovieView(DetailView):
    model = Movie
    template_name = 'pages/movie.html'

    def get_context_data(self, **kwargs):
        context = {
            'movie': self.object,
            'opinion_list': self.get_opinions(),
        }
        context.update(kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.prefetch_related('localizations')

    def get_opinions(self):
        friends = get_friends(self.request.user)
        all_opinions = self.object.opinions.select_related('author')
        friend_opinions = all_opinions.filter(author__in=friends)
        other_opinions = all_opinions.exclude(author__in=friends)
        return chain(friend_opinions, other_opinions)
