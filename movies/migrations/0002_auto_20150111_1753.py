# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titletranslation',
            name='language',
            field=models.CharField(max_length=36),
            preserve_default=True,
        ),
    ]
