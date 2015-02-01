from django.db import models
from django.conf import settings

from djorm_pgarray.fields import ArrayField


class FriendList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='friend_lists')
    provider = models.CharField(max_length=32)
    uids = ArrayField('character varying(255)')

    class Meta:
        unique_together = ('user', 'provider')

    def __str__(self):
        return "{user}'s friends on {provider}".format(
            provider=self.provider, user=self.user)
