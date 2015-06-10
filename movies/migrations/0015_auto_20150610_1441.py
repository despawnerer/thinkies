# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_auto_20150607_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poster',
            old_name='image',
            new_name='local_image',
        ),
        migrations.RenameField(
            model_name='poster',
            old_name='image_updated',
            new_name='local_image_updated',
        ),
    ]
