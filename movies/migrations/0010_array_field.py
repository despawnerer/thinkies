# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20150215_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localization',
            name='aliases',
            field=django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=255)),
        ),
    ]
