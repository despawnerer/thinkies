# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20150111_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='country',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='last_data_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='last_rating_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='mpaa_rating',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
