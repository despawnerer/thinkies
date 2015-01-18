from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .models import Tip


class TipView(DetailView):
    model = Tip
    context_object_name = 'tip'
    template_name = 'tips/detail.html'


class TipListView(ListView):
    model = Tip
    context_object_name = 'tip_list'
    template_name = 'tips/list.html'


class CreateTipView(ModelFormMixin, ProcessFormView):
    http_method_names = ['post']
    model = Tip
    fields = ('movie', 'text',)

    def post(self, request):
        self.object = Tip(author=request.user)
        return super(CreateTipView, self).post(request)
