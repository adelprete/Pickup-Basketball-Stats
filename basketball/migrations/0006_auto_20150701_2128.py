# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0005_auto_20150701_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(max_length=30, choices=[('pot_ast', 'POT'), ('asts', 'AST')], blank=True),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='primary_play',
            field=models.CharField(max_length=30, choices=[('fgm', 'FGM'), ('fga', 'FGA'), ('threepm', '3PM'), ('threepa', '3PA'), ('stls', 'STL'), ('blk', 'BLK'), ('to', 'TO')]),
        ),
    ]
