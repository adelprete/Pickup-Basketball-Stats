# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0007_auto_20150703_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.CharField(null=True, choices=[('5v5', '5v5'), ('4v4', '4v4'), ('3v3', '3v3'), ('2v2', '2v2'), ('1v1', '1v1')], max_length=30),
        ),
        migrations.AddField(
            model_name='statline',
            name='def_pos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='off_pos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='total_pos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(related_name='team2_set', to='basketball.Player', default=[18]),
        ),
    ]
