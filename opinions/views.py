from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .models import Opinion


class OpinionView(DetailView):
    model = Opinion
    context_object_name = 'opinion'
    template_name = 'opinions/detail.html'


class CreateOpinionView(ModelFormMixin, ProcessFormView):
    http_method_names = ['post']
    model = Opinion
    fields = ('movie', 'rating', 'tip',)

    def post(self, request):
        self.object = Opinion(author=request.user)
        return super(CreateOpinionView, self).post(request)
