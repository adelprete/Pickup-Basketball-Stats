# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0006_auto_20150701_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='team1_def_rebounds',
        ),
        migrations.RemoveField(
            model_name='game',
            name='team1_off_rebounds',
        ),
        migrations.RemoveField(
            model_name='game',
            name='team2_def_rebounds',
        ),
        migrations.RemoveField(
            model_name='game',
            name='team2_off_rebounds',
        ),
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(to='basketball.Player', related_name='team1_set', default=[17]),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(choices=[('pot_ast', 'Pot'), ('asts', 'Ast')], max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='primary_play',
            field=models.CharField(choices=[('fgm', 'FGM'), ('fga', 'FGA'), ('threepm', '3PM'), ('threepa', '3PA'), ('blk', 'BLK'), ('to', 'TO'), ('pf', 'FOUL')], max_length=30),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='secondary_play',
            field=models.CharField(choices=[('dreb', 'DREB'), ('oreb', 'OREB'), ('stls', 'STL'), ('ba', 'BA'), ('fd', 'FD')], max_length=30, blank=True),
        ),
    ]
