# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0009_auto_20150714_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['first_name']},
        ),
        migrations.AddField(
            model_name='statline',
            name='def_reb_opp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(to='basketball.Player', default=[5], related_name='team1_set'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(to='basketball.Player', default=[6], related_name='team2_set'),
        ),
    ]
