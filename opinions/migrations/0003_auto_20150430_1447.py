# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0010_array_field'),
        ('opinions', '0002_array_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=140)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(related_name='tips', to='movies.Movie')),
            ],
            options={
                'ordering': ('-creation_date',),
            },
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='author',
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='movie',
        ),
        migrations.DeleteModel(
            name='Opinion',
        ),
    ]
