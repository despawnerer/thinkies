from operator import itemgetter
from requests_oauthlib import OAuth2Session

from django.conf import settings

from .base import Service


class Facebook(Service):
    version = '2.2'
    base_url = 'https://graph.facebook.com/v%s' % version

    def __init__(self, client_id, token):
        self.session = OAuth2Session(client_id, token={
            'access_token': token})

    @classmethod
    def create_for_user(cls, user):
        association = user.social_auth.get(provider='facebook')
        instance = cls(
            settings.SOCIAL_AUTH_FACEBOOK_KEY,
            association.tokens)
        instance.user = user
        instance.association = association
        return instance

    def get_friends(self, user_id):
        friends = []
        next_url = self._build_url('me/friends') + '?fields=id'
        while next_url:
            response = self.session.get(next_url)
            result = self._handle_response(response)
            friends += list(map(itemgetter('id'), result['data']))
            next_url = result.get('paging', {}).get('next')
        return friends

    def get(self, path, **params):
        url = self._build_url(path)
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        response.raise_for_status()
        return response.json()

    def _build_url(self, path):
        return '%s/%s' % (self.base_url, path)
