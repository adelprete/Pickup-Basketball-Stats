# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0030_game_top_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='exhibition',
            field=models.BooleanField(default=False),
        ),
    ]
