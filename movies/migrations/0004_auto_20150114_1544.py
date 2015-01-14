# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20150114_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='mpaa_rating',
            field=models.CharField(max_length=24),
            preserve_default=True,
        ),
    ]
