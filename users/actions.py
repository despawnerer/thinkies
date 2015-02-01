from functools import reduce
from operator import or_

from django.db.models import Q
from django.contrib.auth import get_user_model

import services

from .models import FriendList


__all__ = ['get_friends', 'update_friends']


def get_friends(user):
    User = get_user_model()
    if not user.is_authenticated():
        return User.objects.none()

    queries = [
        Q(social_auth__provider=f.provider, social_auth__uid__in=f.uids)
        for f in user.friend_lists.all()]

    if queries:
        return User.objects.filter(reduce(or_, queries))
    else:
        return User.objects.none()


def update_friends(user, provider):
    if provider not in services.by_provider:
        return

    Service = services.by_provider[provider]
    service = Service.create_for_user(user)
    friend_uids = service.get_friends(service.association.uid)
    FriendList.objects.update_or_create(
        user=user, provider=provider, defaults={'uids': friend_uids})
