# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0040_auto_20160422_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordStatline',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('fgm', models.PositiveIntegerField(default=0)),
                ('fga', models.PositiveIntegerField(default=0)),
                ('threepm', models.PositiveIntegerField(default=0)),
                ('threepa', models.PositiveIntegerField(default=0)),
                ('dreb', models.PositiveIntegerField(default=0)),
                ('oreb', models.PositiveIntegerField(default=0)),
                ('total_rebounds', models.PositiveIntegerField(default=0)),
                ('asts', models.PositiveIntegerField(default=0)),
                ('pot_ast', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('ba', models.PositiveIntegerField(default=0)),
                ('stls', models.PositiveIntegerField(default=0)),
                ('to', models.PositiveIntegerField(default=0)),
                ('fd', models.PositiveIntegerField(default=0)),
                ('pf', models.PositiveIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
                ('ast_points', models.PositiveIntegerField(default=0)),
                ('def_pos', models.PositiveIntegerField(default=0)),
                ('off_pos', models.PositiveIntegerField(default=0)),
                ('total_pos', models.PositiveIntegerField(default=0)),
                ('dreb_opp', models.PositiveIntegerField(default=0)),
                ('oreb_opp', models.PositiveIntegerField(default=0)),
                ('ast_fgm', models.PositiveIntegerField(default=0)),
                ('ast_fga', models.PositiveIntegerField(default=0)),
                ('unast_fgm', models.PositiveIntegerField(default=0)),
                ('unast_fga', models.PositiveIntegerField(default=0)),
                ('pga', models.PositiveIntegerField(default=0)),
                ('pgm', models.PositiveIntegerField(default=0)),
                ('fastbreaks', models.PositiveIntegerField(default=0)),
                ('fastbreak_points', models.PositiveIntegerField(default=0)),
                ('second_chance_points', models.PositiveIntegerField(default=0)),
                ('game_type', models.CharField(choices=[('5v5', '5on5'), ('4v4', '4on4'), ('3v3', '3on3'), ('2v2', '2on2'), ('1v1', '1on1')], max_length=30)),
                ('record_type', models.CharField(choices=[('game', 'Game'), ('day', 'day'), ('season', 'Season')], max_length=30)),
                ('player', models.ForeignKey(to='basketball.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='dailystatline',
            name='gp',
            field=models.PositiveIntegerField(verbose_name='Games Played', default=0),
        ),
        migrations.AlterField(
            model_name='seasonstatline',
            name='gp',
            field=models.PositiveIntegerField(verbose_name='Games Played', default=0),
        ),
    ]
