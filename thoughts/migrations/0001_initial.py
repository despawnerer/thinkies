# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thoughts.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('imdb_url', models.URLField(validators=[thoughts.validators.validate_imdb_url])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=140)),
                ('movie', models.ForeignKey(to='thoughts.Movie')),
            ],
            options={
                'ordering': ('-created_at',),
                'get_latest_by': 'created_at',
            },
            bases=(models.Model,),
        ),
    ]
