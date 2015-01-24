# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20150114_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheatricalDay',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('movie', models.ForeignKey(to_field='imdb_id', to='movies.Movie', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, related_name='theatrical_days', db_column='imdb_id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='theatricalday',
            unique_together=set([('movie', 'country', 'city', 'date')]),
        ),
    ]
