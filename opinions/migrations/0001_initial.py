# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0007_auto_20150124_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField(null=True, choices=[(0, 'No'), (5, 'It was OK'), (10, 'Yes!')])),
                ('tip', models.CharField(blank=True, max_length=140)),
                ('adjectives', djorm_pgarray.fields.ArrayField(dbtype='character varying(255)')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(related_name='opinions', to='movies.Movie')),
            ],
            options={
                'ordering': ('-creation_date',),
            },
            bases=(models.Model,),
        ),
    ]
