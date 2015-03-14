from requests_oauthlib import OAuth1Session

from django.conf import settings

from .base import Service, Profile


class Twitter(Service):
    version = '1.1'
    base_url = 'https://api.twitter.com/%s' % version

    def __init__(self, client_key, client_secret, token, token_secret, user_id):
        self.session = OAuth1Session(
            client_key, client_secret=client_secret, resource_owner_key=token,
            resource_owner_secret=token_secret)
        self.user_id = user_id

    @classmethod
    def create_for_user(cls, user):
        association = user.social_auth.get(provider='twitter')
        oauth_token = association.tokens['oauth_token']
        oauth_token_secret = association.tokens['oauth_token_secret']

        return cls(
            settings.SOCIAL_AUTH_TWITTER_KEY,
            settings.SOCIAL_AUTH_TWITTER_SECRET,
            oauth_token, oauth_token_secret, association.uid)

    def get_friends(self):
        following = set(self.get_cursored('friends/ids', 'ids',
                                          user_id=self.user_id))
        followers = set(self.get_cursored('followers/ids', 'ids',
                                          user_id=self.user_id))
        muted = set(self.get_cursored('mutes/users/ids', 'ids'))
        return (following & followers) - muted

    def get_profile(self):
        user_info = self.get('users/show', user_id=self.user_id)
        return TwitterProfile(user_info)

    def get_cursored(self, path, result_field, **params):
        results = []
        cursor = -1
        while cursor != 0:
            response = self.get(path, cursor=cursor, **params)
            results += response[result_field]
            cursor = response['next_cursor']
        return results

    def get(self, path, **params):
        url = self._build_url(path)
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        response.raise_for_status()
        return response.json()

    def _build_url(self, path):
        return '%s/%s.json' % (self.base_url, path)


class TwitterProfile(Profile):
    def __init__(self, user_info):
        self.user_info = user_info

    @property
    def uid(self):
        return self.user_info.get('id')

    @property
    def name(self):
        return self.user_info.get('name')

    @property
    def image(self):
        url = self.user_info.get('profile_image_url')
        if url:
            return url.replace('_normal', '')
