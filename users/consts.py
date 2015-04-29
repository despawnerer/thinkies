from django.utils.translation import ugettext_lazy as _


AUTH_BACKEND_DETAILS = {
    'vk-oauth2': {
        'name': 'vk',
        'verbose_name': _("VKontakte"),
    },
    'facebook': {
        'name': 'facebook',
        'verbose_name': _("Facebook"),
    },
    'twitter': {
        'name': 'twitter',
        'verbose_name': _("Twitter"),
    }
}


AUTH_BACKEND_ORDER_DEFAULT = ['facebook', 'twitter', 'vk-oauth2']
AUTH_BACKEND_ORDER_BY_LANGUAGE = {
    'ru': ['vk-oauth2', 'twitter', 'facebook']
}
