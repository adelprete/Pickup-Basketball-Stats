# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='team1_team_rebounds',
            new_name='team1_def_rebounds',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='team2_team_rebounds',
            new_name='team1_off_rebounds',
        ),
        migrations.AddField(
            model_name='game',
            name='team2_def_rebounds',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='team2_off_rebounds',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(max_length=30, choices=[('ast', 'AST'), ('pot', 'POT')]),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='primary_play',
            field=models.CharField(max_length=30, choices=[('fgm', 'FGM'), ('fga', 'FGA'), ('3pm', '3PM'), ('3pa', '3PA'), ('stl', 'STL'), ('blk', 'BLK'), ('to', 'TO')]),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='secondary_play',
            field=models.CharField(blank=True, choices=[('dreb', 'DREB'), ('oreb', 'OREB'), ('ba', 'BA')], max_length=30),
        ),
    ]
