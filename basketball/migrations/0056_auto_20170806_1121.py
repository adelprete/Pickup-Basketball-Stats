# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('basketball', '0055_game_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='group',
            field=models.ForeignKey(on_delete=models.CASCADE, to='base.Group', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='group',
            field=models.ForeignKey(on_delete=models.CASCADE, to='base.Group', blank=True, null=True),
        ),
    ]
