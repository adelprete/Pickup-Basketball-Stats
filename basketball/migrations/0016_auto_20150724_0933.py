# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0015_auto_20150723_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='playbyplay',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='top_play_players',
            field=models.ManyToManyField(to='basketball.Player', blank=True),
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='top_play_rank',
            field=models.CharField(choices=[('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'), ('t4', 'T4'), ('t5', 'T5'), ('t6', 'T6'), ('t7', 'T7'), ('t8', 'T8'), ('t9', 'T9'), ('t10', 'T10'), ('nt1', 'NT1'), ('nt2', 'NT2'), ('nt3', 'NT3'), ('nt4', 'NT4'), ('nt5', 'NT5'), ('nt6', 'NT6'), ('nt7', 'NT7'), ('nt8', 'NT8'), ('nt9', 'NT9'), ('nt10', 'NT10')], max_length=30, blank=True),
        ),
    ]
