# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_remove_localization_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='localization',
            name='poster',
            field=models.OneToOneField(to='movies.Poster', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
