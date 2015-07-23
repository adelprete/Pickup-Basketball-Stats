# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0014_game_winning_players'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-date', 'title']},
        ),
        migrations.AlterField(
            model_name='game',
            name='winning_players',
            field=models.ManyToManyField(blank=True, related_name='winning_players_set', to='basketball.Player'),
        ),
    ]
