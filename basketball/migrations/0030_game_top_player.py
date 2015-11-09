# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0029_auto_20151027_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='top_player',
            field=models.ForeignKey(related_name='top_player_set', blank=True, null=True, to='basketball.Player'),
        ),
    ]
