from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class Tip(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('movies.Movie', related_name='tips')
    text = models.CharField(max_length=140)

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('tips:tip', kwargs={'pk': self.pk})
