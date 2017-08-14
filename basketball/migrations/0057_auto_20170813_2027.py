# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0056_auto_20170806_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='fastbreak_window',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='game',
            name='putback_window',
            field=models.PositiveIntegerField(default=6),
        ),
    ]
