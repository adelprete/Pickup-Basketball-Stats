# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0045_auto_20160530_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablematrix',
            name='game_type',
            field=models.CharField(default='', choices=[('5v5', '5on5'), ('4v4', '4on4'), ('3v3', '3on3'), ('2v2', '2on2'), ('1v1', '1on1')], max_length=30),
        ),
    ]
