from django.apps import AppConfig

from .signals import social_auth_complete
from .receivers import update_friends_on_auth


class UsersAppConfig(AppConfig):
    name = 'users'

    def ready(self):
        social_auth_complete.connect(update_friends_on_auth)
