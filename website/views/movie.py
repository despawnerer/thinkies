from itertools import chain

from django.views.generic import DetailView

from users.actions import get_friends

from opinions.models import Tip

from movies.models import Movie

from ..forms.tip import TipForm


class MovieView(DetailView):
    model = Movie
    template_name = 'pages/movie.jinja2'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        tip_form = self.get_tip_form()
        return self.render_to_response(
            self.get_context_data(tip_form=tip_form))

    def post(self, request, **kwargs):
        self.object = self.get_object()
        tip_form = self.get_tip_form()
        if tip_form.is_valid():
            tip_form.save()
        return self.render_to_response(
            self.get_context_data(tip_form=tip_form))

    def get_context_data(self, **kwargs):
        context = {
            'movie': self.object,
            'tip_list': self.get_tips(),
        }
        context.update(kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.prefetch_related('localizations')

    def get_tips(self):
        friends = get_friends(self.request.user)
        all_tips = self.object.tips.select_related('author')
        friend_tips = all_tips.filter(author__in=friends)
        other_tips = all_tips.exclude(author__in=friends)
        return chain(friend_tips, other_tips)

    def get_tip_form(self):
        if self.request.user.is_authenticated():
            tip = Tip(author=self.request.user, movie=self.object)
        else:
            tip = Tip(movie=self.object)
        return TipForm(instance=tip, data=self.request.POST)
