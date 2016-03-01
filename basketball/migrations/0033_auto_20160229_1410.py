# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0032_auto_20160124_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='fastbreak_points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='fastbreaks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
