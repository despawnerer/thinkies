# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20150607_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('source_url', models.URLField(null=True)),
                ('source_updated', models.DateTimeField(null=True)),
                ('image', models.ImageField(null=True, upload_to='', height_field='height', width_field='field')),
                ('image_updated', models.DateTimeField(null=True)),
                ('width', models.PositiveIntegerField(null=True)),
                ('height', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.OneToOneField(to='movies.Poster', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
    ]
