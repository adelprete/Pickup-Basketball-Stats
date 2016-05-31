# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0044_tablematrix_points_to_win'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablematrix',
            name='title',
        ),
        migrations.AddField(
            model_name='tablematrix',
            name='season',
            field=models.ForeignKey(null=True, to='basketball.Season', blank=True),
        ),
        migrations.AddField(
            model_name='tablematrix',
            name='type',
            field=models.CharField(max_length=30, choices=[('game_records', 'Game Records'), ('day_records', 'Day Records'), ('season_records', 'Season Records')], default=''),
        ),
        migrations.AlterField(
            model_name='tablematrix',
            name='points_to_win',
            field=models.CharField(max_length=30, choices=[('11', '11'), ('30', '30'), ('other', 'Other')], default=''),
        ),
    ]
