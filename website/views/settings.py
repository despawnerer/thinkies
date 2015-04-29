from django.views.generic import TemplateView


class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    def get_context_data(self, **kwargs):
        identities = self.request.user.identities.all()
        context = {
            'identities': identities,
        }
        context.update(kwargs)
        return context
