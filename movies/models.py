from funcy import cached_property

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.translation import get_language

from djorm_pgarray.fields import ArrayField


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    mpaa_rating = models.CharField(max_length=24)
    release_date = models.DateField(null=True)
    poster = models.ImageField(null=True)

    imdb_id = models.CharField(max_length=50, unique=True)
    imdb_rating = models.FloatField(null=True)
    imdb_votes = models.IntegerField(null=True)

    last_data_update = models.DateTimeField(null=True)
    last_rating_update = models.DateTimeField(null=True)

    def __str__(self):
        return _("{title} ({year})").format(title=self.translated_title,
                                            year=self.year)

    def get_absolute_url(self):
        return reverse('movies:movie', kwargs={'pk': self.pk})

    @property
    def imdb_url(self):
        return 'http://www.imdb.com/title/%s' % self.imdb_id

    @property
    def is_released(self):
        today = timezone.now().date()
        if self.release_date:
            return self.release_date <= today
        else:
            return self.year < today.year

    @property
    def translated_title(self):
        return self.localization.title if self.localization else self.title

    @cached_property
    def localization(self):
        return self.localizations_by_language.get(get_language())

    @cached_property
    def localizations_by_language(self):
        return {t.language: t.title for t in self.localizations.all()}


class Localization(models.Model):
    movie = models.ForeignKey(Movie, to_field='imdb_id', db_constraint=False,
                              db_column='imdb_id', on_delete=models.DO_NOTHING,
                              related_name='localizations')
    language = models.CharField(max_length=36)

    title = models.CharField(max_length=255)
    description = models.TextField()
    aliases = ArrayField('character varying(255)', null=False, default='{}')
    poster = models.ImageField(null=True)
    wikipedia_page = models.CharField(max_length=1024)

    class Meta:
        unique_together = ('movie', 'language')

    def __str__(self):
        return '%s (%s)' % (self.title, self.language)


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
