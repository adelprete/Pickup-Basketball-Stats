# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0058_auto_20170814_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='outdated',
            field=models.BooleanField(default=True),
        ),
    ]
