# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0023_auto_20150908_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.CharField(choices=[('5v5', '5on5'), ('4v4', '4on4'), ('3v3', '3on3'), ('2v2', '2on2'), ('1v1', '1on1')], max_length=30, null=True),
        ),
    ]
