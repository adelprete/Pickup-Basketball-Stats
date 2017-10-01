# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0061_player_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='score_type',
            field=models.CharField(choices=[('1and2', "1's and 2's"), ('2and3', "2's and 3's")], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Determine if a player should be selectable when creating games'),
        ),
    ]
