# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20150215_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='localization',
            name='aliases',
            field=djorm_pgarray.fields.ArrayField(default='{}', dbtype='character varying(255)', null=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localization',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localization',
            name='poster',
            field=models.ImageField(upload_to='', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localization',
            name='wikipedia_page',
            field=models.CharField(max_length=1024, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='localization',
            name='movie',
            field=models.ForeignKey(to_field='imdb_id', db_column='imdb_id', on_delete=django.db.models.deletion.DO_NOTHING, to='movies.Movie', db_constraint=False, related_name='localizations'),
            preserve_default=True,
        ),
    ]
