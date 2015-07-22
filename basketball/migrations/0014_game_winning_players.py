# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0013_auto_20150716_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winning_players',
            field=models.ManyToManyField(to='basketball.Player', blank=True, null=True, related_name='winning_players_set'),
        ),
    ]
