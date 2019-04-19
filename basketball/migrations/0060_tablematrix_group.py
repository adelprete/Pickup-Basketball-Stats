# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20170820_1043'),
        ('basketball', '0059_game_outdated'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablematrix',
            name='group',
            field=models.ForeignKey(on_delete=models.CASCADE, null=True, to='base.Group'),
        ),
    ]
