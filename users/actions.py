from functools import reduce
from operator import or_
from funcy import merge, collecting

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import get_language

import services

from thinkies.utils import load_url

from .models import Identity
from .consts import (
    AUTH_BACKEND_DETAILS,
    AUTH_BACKEND_ORDER_BY_LANGUAGE,
    AUTH_BACKEND_ORDER_DEFAULT,
)


__all__ = [
    'get_auth_providers', 'get_friends', 'update_identity'
]


@collecting
def get_auth_providers(user):
    if user and user.is_authenticated():
        associated_backends = {i.provider for i in user.identities.all()}
    else:
        associated_backends = set()

    language = get_language()
    backend_name_list = AUTH_BACKEND_ORDER_BY_LANGUAGE.get(
        language, AUTH_BACKEND_ORDER_DEFAULT)
    for backend_name in backend_name_list:
        details = AUTH_BACKEND_DETAILS.get(backend_name)
        yield merge(details, {
            'backend_name': backend_name,
            'is_associated': backend_name in associated_backends,
        })


def get_friends(user):
    # TODO: cache the queryset on user instance
    User = get_user_model()
    if not user.is_authenticated():
        return User.objects.none()

    queries = [
        Q(social_auth__provider=identity.provider,
          social_auth__uid__in=identity.friend_uids)
        for identity in user.identities.all()]

    if queries:
        return User.objects.filter(reduce(or_, queries))
    else:
        return User.objects.none()


def update_identity(user, provider):
    if provider not in services.by_provider:
        return

    Service = services.by_provider[provider]
    service = Service.create_for_user(user)

    friend_uids = service.get_friends()
    profile = service.get_profile()
    Identity.objects.update_or_create(
        user=user, provider=provider, defaults={
            'uid': profile.uid,
            'friend_uids': list(friend_uids),
            'name': profile.name,
            'image': load_url(profile.image,
                              'identity_{}_{}'.format(user.pk, provider)),
        })
