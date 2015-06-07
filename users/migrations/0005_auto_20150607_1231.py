# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thinkies.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150429_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identity',
            name='image',
            field=models.ImageField(null=True, upload_to=thinkies.utils.get_hashed_file_upload_path),
        ),
    ]
