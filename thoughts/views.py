from django.views.generic.list import ListView

from .models import Thought


class Index(ListView):
    model = Thought
    template_name = 'index.html'
