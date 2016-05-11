# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0039_dailystatline_seasonstatline'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailystatline',
            name='gp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seasonstatline',
            name='gp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
