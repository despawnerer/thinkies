# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20150607_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.ImageField(upload_to='', width_field='width', height_field='height', null=True),
        ),
    ]
