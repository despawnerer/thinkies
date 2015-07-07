from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from ..forms.settings import SettingsForm

from .mixins import PrivateViewMixin


class SettingsView(PrivateViewMixin, UpdateView):
    template_name = 'pages/settings.jinja2'
    form_class = SettingsForm
    success_url = reverse_lazy('site:settings')

    def get_context_data(self, **kwargs):
        form = kwargs.get('form')
        context = super().get_context_data(**kwargs)
        context.update({
            'identities': self.identities,
            'identity_widgets': zip(self.identities, form['default_identity'])
        })
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['identities'] = self.identities
        return form_kwargs

    def get_object(self):
        user = self.request.user
        self.identities = user.identities.all()
        return user
