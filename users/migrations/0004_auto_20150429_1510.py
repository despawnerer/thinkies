# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_array_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='identity',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='default_identity',
            field=models.OneToOneField(related_name='+', to='users.Identity', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
