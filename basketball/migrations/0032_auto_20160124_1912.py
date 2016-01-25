# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0031_game_exhibition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='exhibition',
            field=models.BooleanField(default=False, help_text='Stats for Exhibition games are NOT counted.', verbose_name='Exhibition Game?'),
        ),
    ]
