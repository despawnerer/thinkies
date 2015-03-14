from functools import reduce
from operator import or_
from urllib.request import urlopen

from django.core.files.base import ContentFile
from django.db.models import Q
from django.contrib.auth import get_user_model

import services

from .models import Identity


__all__ = ['get_friends', 'update_identity']


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
            'friend_uids': friend_uids,
            'name': profile.name,
            'image': _load_url(profile.image,
                               '{}_{}'.format(provider, user.pk)),
        })


def _load_url(url, name):
    if url is None:
        return None

    # TODO: error handling
    url_content = urlopen(url)
    type_ = url_content.headers.get_content_subtype()
    full_name = '{}.{}'.format(name, type_)
    return ContentFile(url_content.read(), full_name)
