# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_parsedmovie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parsedmovie',
            name='movie',
            field=models.ForeignKey(to_field='imdb_id', on_delete=django.db.models.deletion.DO_NOTHING, db_column='imdb_id', related_name='+', db_constraint=False, null=True, to='movies.Movie'),
            preserve_default=True,
        ),
    ]
