from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from thinkies.utils import get_hashed_file_upload_path


class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        return self.create_user(email, password, True, True)

    def create_user(self, email=None, password=None,
                    is_staff=False, is_superuser=False):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    default_identity = models.OneToOneField(
        'Identity', null=True, related_name='+', on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.default_identity:
            return self.default_identity.name
        else:
            return self.email or str(self.pk)


class Identity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='identities')
    provider = models.CharField(max_length=32)

    uid = models.CharField(max_length=255)
    friend_uids = ArrayField(models.CharField(max_length=255), default=[])
    name = models.CharField(max_length=255)
    image = models.ImageField(
        null=True, upload_to=get_hashed_file_upload_path)

    class Meta:
        ordering = ('name',)
        unique_together = ('user', 'provider')

    def __str__(self):
        return "{user} on {provider}".format(
            user=self.user, provider=self.provider)
