from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from social.backends.utils import load_backends
from social.apps.django_app.utils import BACKENDS


PROVIDER_NAMES = {
    'vk-oauth2': 'vk',
    'facebook': 'facebook',
    'twitter': 'twitter',
}

PROVIDER_VERBOSE_NAMES = {
    'vk-oauth2': _("VKontakte"),
    'facebook': _("Facebook"),
    'twitter': _("Twitter"),
}


class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    def get_context_data(self, **kwargs):
        identities = self.request.user.identities.all()
        provider_details = self.get_provider_details(identities)
        context = {
            'identities': identities,
            'provider_details': provider_details,
        }
        context.update(kwargs)
        return context

    def get_provider_details(self, identities):
        associated_backends = {i.provider for i in identities}
        backends = load_backends(BACKENDS)
        provider_details = []
        for backend_name in backends.keys():
            provider_details.append({
                'backend_name': backend_name,
                'name': PROVIDER_NAMES.get(backend_name, backend_name),
                'verbose_name': PROVIDER_VERBOSE_NAMES.get(
                    backend_name, backend_name),
                'is_associated': backend_name in associated_backends,
            })
        return provider_details
