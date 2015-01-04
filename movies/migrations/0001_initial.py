# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(unique=True, max_length=50)),
                ('imdb_rating', models.FloatField(null=True)),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
                ('poster', models.ImageField(null=True, upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('movie', models.ForeignKey(db_constraint=False, to='movies.Movie', to_field='imdb_id', db_column='imdb_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='title_translations')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='titletranslation',
            unique_together=set([('movie', 'language')]),
        ),
    ]
