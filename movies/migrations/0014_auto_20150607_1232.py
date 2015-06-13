# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thinkies.utils


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_auto_20150607_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.ImageField(upload_to=thinkies.utils.get_hashed_file_upload_path, height_field='height', null=True, width_field='width'),
        ),
    ]
