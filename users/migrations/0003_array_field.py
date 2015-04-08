# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_django_18'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='friend_uids',
            field=django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=255)),
        ),
    ]
