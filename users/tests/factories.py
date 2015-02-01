import factory

from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "User #%d" % n)


class UserSocialAuthFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = UserSocialAuth
