# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_array_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster',
        ),
    ]
