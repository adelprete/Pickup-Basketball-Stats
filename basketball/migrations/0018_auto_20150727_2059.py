# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0017_auto_20150724_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbyplay',
            name='primary_play',
            field=models.CharField(max_length=30, choices=[('fgm', 'FGM'), ('fga', 'FGA'), ('threepm', '3PM'), ('threepa', '3PA'), ('blk', 'BLK'), ('to', 'TO'), ('pf', 'FOUL'), ('sub_out', 'OUT'), ('misc', 'Misc')]),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='top_play_rank',
            field=models.CharField(max_length=30, choices=[('t01', 'T1'), ('t02', 'T2'), ('t03', 'T3'), ('t04', 'T4'), ('t05', 'T5'), ('t06', 'T6'), ('t07', 'T7'), ('t08', 'T8'), ('t09', 'T9'), ('t10', 'T10'), ('nt01', 'NT1'), ('nt02', 'NT2'), ('nt03', 'NT3'), ('nt04', 'NT4'), ('nt05', 'NT5'), ('nt06', 'NT6'), ('nt07', 'NT7'), ('nt08', 'NT8'), ('nt09', 'NT9'), ('nt10', 'NT10')], help_text='Refers to weekly rank', blank=True),
        ),
    ]
