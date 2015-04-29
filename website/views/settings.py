from django.views.generic import TemplateView

from ..forms.settings import SettingsForm


class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        identities = user.identities.all()
        form = SettingsForm(identities, instance=user)
        context = {
            'form': form,
            'identities': identities,
            'identity_widgets': zip(identities, form['default_identity'])
        }
        context.update(kwargs)
        return context
