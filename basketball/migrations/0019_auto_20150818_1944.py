# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0018_auto_20150727_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(default=[], related_name='team1_set', to='basketball.Player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(default=[], related_name='team2_set', to='basketball.Player'),
        ),
    ]
