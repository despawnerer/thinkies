from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class Opinion(models.Model):
    NEGATIVE = 0
    NEUTRAL = 5
    POSITIVE = 10
    RATING_CHOICES = (
        (NEGATIVE, _("No")),
        (NEUTRAL, _("It was OK")),
        (POSITIVE, _("Yes!"))
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True)

    movie = models.ForeignKey('movies.Movie', related_name='opinions')

    rating = models.PositiveSmallIntegerField(
        null=True, choices=RATING_CHOICES)
    tip = models.CharField(max_length=140, blank=True)
    adjectives = ArrayField(models.CharField(max_length=255), default=[])

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return self.tip

    def get_absolute_url(self):
        return reverse('opinions:opinion', kwargs={'pk': self.pk})
