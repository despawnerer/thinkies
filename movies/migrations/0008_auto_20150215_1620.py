# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20150124_2105'),
    ]

    operations = [
        migrations.RenameModel('TitleTranslation', 'Localization')
    ]
