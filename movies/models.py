from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.contrib.postgres.fields import ArrayField

from thinkies.utils import get_hashed_file_upload_path
from .utils import lens


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    mpaa_rating = models.CharField(max_length=24)
    release_date = models.DateField(null=True)
    poster = models.OneToOneField(
        'Poster', null=True, on_delete=models.SET_NULL)

    imdb_id = models.CharField(max_length=50, unique=True)
    imdb_rating = models.FloatField(null=True)
    imdb_votes = models.IntegerField(null=True)

    last_data_update = models.DateTimeField(null=True)
    last_rating_update = models.DateTimeField(null=True)

    def __str__(self):
        return _("{title} ({year})").format(title=self.translated.title,
                                            year=self.year)

    @lens
    def translated(self):
        return self.localizations_by_language.get(get_language())

    @property
    def imdb_url(self):
        return 'http://www.imdb.com/title/%s' % self.imdb_id


    @property
    def localizations_by_language(self):
        return {l.language: l for l in self.localizations.all()}


class Localization(models.Model):
    movie = models.ForeignKey(Movie, to_field='imdb_id', db_constraint=False,
                              db_column='imdb_id', on_delete=models.DO_NOTHING,
                              related_name='localizations')
    language = models.CharField(max_length=36)

    title = models.CharField(max_length=255)
    description = models.TextField()
    aliases = ArrayField(models.CharField(max_length=255), default=[])
    poster = models.ImageField(null=True)
    wikipedia_page = models.CharField(max_length=1024)

    class Meta:
        unique_together = ('movie', 'language')

    def __str__(self):
        return '%s (%s)' % (self.title, self.language)

    @property
    def wikipedia_url(self):
        return '//{}.wikipedia.org/wiki/{}'.format(
            self.language, self.wikipedia_page)


class Poster(models.Model):
    source_url = models.URLField(null=True)
    source_updated = models.DateTimeField(null=True)

    image = models.ImageField(
        null=True, width_field='width', height_field='height',
        upload_to=get_hashed_file_upload_path)
    image_updated = models.DateTimeField(null=True)

    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)


class TheatricalDay(models.Model):
    movie = models.ForeignKey(Movie, to_field='imdb_id', db_constraint=False,
                              db_column='imdb_id', on_delete=models.DO_NOTHING,
                              related_name='theatrical_days')
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    date = models.DateField()

    class Meta:
        unique_together = ('movie', 'country', 'city', 'date')


class ParsedMovie(models.Model):
    title = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)
    additional_data = models.TextField()

    movie = models.ForeignKey(Movie, to_field='imdb_id', db_constraint=False,
                              db_column='imdb_id', on_delete=models.DO_NOTHING,
                              related_name='+', null=True)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return '{} (id: {})'.format(self.title, self.source_id)
