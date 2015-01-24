# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20150124_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParsedMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('source_id', models.CharField(max_length=255)),
                ('additional_data', models.TextField()),
                ('is_rejected', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(db_column='imdb_id', to='movies.Movie', db_constraint=False, related_name='+', to_field='imdb_id', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
