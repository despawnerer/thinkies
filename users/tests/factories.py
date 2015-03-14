import factory

from users.models import User

from social.apps.django_app.default.models import UserSocialAuth


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User


class UserSocialAuthFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = UserSocialAuth
