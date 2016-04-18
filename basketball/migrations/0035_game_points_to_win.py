# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0034_statline_second_chance_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='points_to_win',
            field=models.CharField(max_length=30, default='11', choices=[('11', '11'), ('30', '30'), ('other', 'Other')]),
        ),
    ]
