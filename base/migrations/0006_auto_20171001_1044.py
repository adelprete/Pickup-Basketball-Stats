# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20170820_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='game_type',
            field=models.CharField(choices=[('5v5', '5on5'), ('4v4', '4on4'), ('3v3', '3on3'), ('2v2', '2on2'), ('1v1', '1on1')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='score_type',
            field=models.CharField(choices=[('1and2', "1's and 2's"), ('2and3', "2's and 3's")], max_length=30, null=True),
        ),
    ]
