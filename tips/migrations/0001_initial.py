# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0004_auto_20150114_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=140)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(to='movies.Movie', related_name='tips')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
