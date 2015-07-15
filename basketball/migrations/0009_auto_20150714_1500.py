# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0008_auto_20150710_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbyplay',
            name='primary_play',
            field=models.CharField(choices=[('fgm', 'FGM'), ('fga', 'FGA'), ('threepm', '3PM'), ('threepa', '3PA'), ('blk', 'BLK'), ('to', 'TO'), ('pf', 'FOUL'), ('sub_out', 'OUT')], max_length=30),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='secondary_play',
            field=models.CharField(blank=True, choices=[('dreb', 'DREB'), ('oreb', 'OREB'), ('stls', 'STL'), ('ba', 'BA'), ('fd', 'FD'), ('sub_in', 'IN')], max_length=30),
        ),
    ]
