# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_auto_20150610_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localization',
            name='poster',
        ),
    ]
