# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0047_seasonper100statline'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonper100statline',
            name='player',
            field=models.ForeignKey(null=True, to='basketball.Player'),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='season',
            field=models.ForeignKey(null=True, to='basketball.Season'),
        ),
        migrations.AlterField(
            model_name='tablematrix',
            name='type',
            field=models.CharField(choices=[('game_records', 'Game Records'), ('day_records', 'Day Records'), ('season_records', 'Season Records'), ('season_per100_records', 'Season Per100 Records')], default='', max_length=30),
        ),
    ]
