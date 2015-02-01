from django.test import TestCase

import services

from users.actions import get_friends, update_friends
from users.models import FriendList

from .factories import UserFactory, UserSocialAuthFactory


class GetFriendsTestCase(TestCase):
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


class UpdateFriendsTestCase(TestCase):
    def setUp(self):
        services.by_provider[DUMMY_PROVIDER] = DummyService

    def tearDown(self):
        del services.by_provider[DUMMY_PROVIDER]

    def test_creates_friend_list_when_there_isnt_one(self):
        user = UserFactory.create()
        UserSocialAuthFactory.create(
            provider=DUMMY_PROVIDER, user=user, uid=user.pk)

        self.assertEqual(len(user.friend_lists.all()), 0)
        update_friends(user, DUMMY_PROVIDER)
        friend_list = user.friend_lists.get(provider=DUMMY_PROVIDER)
        self.assertEqual(friend_list.uids, ['1', '2', '3'])

    def test_updates_friend_list_from_service(self):
        user = UserFactory.create()
        UserSocialAuthFactory.create(
            provider=DUMMY_PROVIDER, user=user, uid=user.pk)
        FriendList.objects.create(
            provider=DUMMY_PROVIDER, user=user, uids=['40', '50', '60'])

        update_friends(user, DUMMY_PROVIDER)
        friend_list = user.friend_lists.get(provider=DUMMY_PROVIDER)
        self.assertEqual(friend_list.uids, ['1', '2', '3'])


# a dummy service for our dummy provider

DUMMY_PROVIDER = 'dummy'


class DummyService:
    @classmethod
    def create_for_user(cls, user):
        instance = cls()
        instance.user = user
        instance.association = user.social_auth.get(provider=DUMMY_PROVIDER)
        return instance

    def get_friends(self, user_id):
        return [1, 2, 3]


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
    FriendList.objects.create(provider=provider, user=user,
                              uids=friend_uids)
    return friends
