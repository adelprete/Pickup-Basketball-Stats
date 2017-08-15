# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0057_auto_20170813_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='fastbreak_window',
            field=models.PositiveIntegerField(default=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='putback_window',
            field=models.PositiveIntegerField(default=6, null=True, blank=True),
        ),
    ]
