from django.db import models
from django.conf import settings


class Tip(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ForeignKey('movies.Movie', related_name='tips')
    creation_date = models.DateTimeField(auto_now_add=True)

    text = models.CharField(max_length=140)

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return self.text
