import factory
import random

from movies.models import Movie, Localization


class MovieFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Movie

    imdb_id = factory.Sequence(lambda n: 'tt%07d' % n)
    year = factory.LazyAttribute(lambda x: random.randint(1800, 2055))


class LocalizationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Localization
