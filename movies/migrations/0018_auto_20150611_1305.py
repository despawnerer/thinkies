# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_localization_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='source_url',
            field=models.URLField(null=True, max_length=2048),
        ),
    ]
