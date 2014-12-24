from django.db import models
from django.utils.translation import ugettext_lazy as _

from .validators import validate_imdb_url


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    imdb_url = models.URLField(validators=[validate_imdb_url])

    def __str__(self):
        return _("%(title)s (%(year)d)") % {
            'title': self.title, 'year': self.year}


class Thought(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie)
    text = models.CharField(max_length=140)

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-created_at',)

    def __str__(self):
        return self.text
