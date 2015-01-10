from django.db import models
from django.utils.translation import ugettext_lazy as _


class Movie(models.Model):
    imdb_id = models.CharField(max_length=50, unique=True)
    imdb_rating = models.FloatField(null=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    country = models.CharField(max_length=255)
    poster = models.ImageField(null=True)

    def __str__(self):
        return _("{title} ({year})").format(title=self.title, year=self.year)


class TitleTranslation(models.Model):
    """
    Holds a translated title for a movie, referenced by its imdb id.
    For search and display purposes, mostly.
    """
    # this is really just for the ability to do joins
    movie = models.ForeignKey(Movie, to_field='imdb_id', db_constraint=False,
                              db_column='imdb_id', on_delete=models.DO_NOTHING,
                              related_name='title_translations')
    language = models.CharField(max_length=10)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('movie', 'language')
