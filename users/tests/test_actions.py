from collections import namedtuple

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

import services

from users.actions import get_friends, update_identity
from users.models import Identity

from .factories import UserFactory, UserSocialAuthFactory


class GetFriendsTestCase(TestCase):
    def test_returns_empty_set_for_anonymous_users(self):
        user = AnonymousUser()
        friends = get_friends(user)
        self.assertSetEqual(set(friends), set())

    def test_returns_empty_list_with_no_friends(self):
        user = UserFactory.create()
        friends = get_friends(user)
        self.assertSetEqual(set(friends), set())

    def test_returns_proper_friends_users(self):
        user = UserFactory.create()
        expected_friends = create_unique_friends(user, 'dummy')
        friends = get_friends(user)
        self.assertSetEqual(set(friends), set(expected_friends))

    def test_returns_all_friends_across_providers(self):
        user = UserFactory.create()
        expected_friends1 = create_unique_friends(user, 'one')
        expected_friends2 = create_unique_friends(user, 'two')
        friends = get_friends(user)
        self.assertSetEqual(
            set(friends), set(expected_friends1 + expected_friends2))

    def test_doesnt_return_friends_of_other_users(self):
        user = UserFactory.create()
        other_user = UserFactory.create()
        our_friends = create_unique_friends(user, 'dummy')
        create_unique_friends(other_user, 'dummy')
        friends = get_friends(user)
        self.assertSetEqual(set(friends), set(our_friends))


class UpdateIdentityTestCase(TestCase):
    def setUp(self):
        services.by_provider[DUMMY_PROVIDER] = DummyService

    def tearDown(self):
        del services.by_provider[DUMMY_PROVIDER]

    def test_creates_identity_when_there_isnt_one(self):
        user = UserFactory.create()
        UserSocialAuthFactory.create(
            provider=DUMMY_PROVIDER, user=user, uid='2015')

        self.assertEqual(len(user.identities.all()), 0)

        update_identity(user, DUMMY_PROVIDER)
        identity = user.identities.get(provider=DUMMY_PROVIDER)
        self.assertEqual(identity.uid, '2015')
        self.assertEqual(identity.name, 'Dummy')
        self.assertEqual(identity.friend_uids, ['1', '2', '3'])

    def test_updates_data_from_service(self):
        user = UserFactory.create()
        UserSocialAuthFactory.create(
            provider=DUMMY_PROVIDER, user=user, uid=2015)
        Identity.objects.create(
            provider=DUMMY_PROVIDER, user=user, uid='old', name='Wrong',
            friend_uids=['40', '50'])

        update_identity(user, DUMMY_PROVIDER)
        identity = user.identities.get(provider=DUMMY_PROVIDER)
        self.assertEqual(identity.uid, '2015')
        self.assertEqual(identity.name, 'Dummy')
        self.assertEqual(identity.friend_uids, ['1', '2', '3'])


# a dummy service for our dummy provider

DUMMY_PROVIDER = 'dummy'


class DummyService:
    @classmethod
    def create_for_user(cls, user):
        return cls()

    def get_friends(self):
        return [1, 2, 3]

    def get_profile(self):
        return DummyProfile(2015, 'Dummy', None)


DummyProfile = namedtuple('DummyProfile', ('uid', 'name', 'image'))


# helpers

def create_unique_friends(user, provider, count=5):
    friends = []
    friend_uids = []
    for n in range(count):
        uid = '{}_{}'.format(user.pk, n)
        friend = UserFactory.create()
        UserSocialAuthFactory.create(provider=provider, user=friend, uid=uid)
        friends.append(friend)
        friend_uids.append(uid)
    Identity.objects.create(provider=provider, user=user,
                            friend_uids=friend_uids, uid=user.pk)
    return friends
