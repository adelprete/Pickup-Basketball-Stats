# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0019_auto_20150818_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(to='basketball.Player', related_name='team1_set', default=[5]),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(to='basketball.Player', related_name='team2_set', default=[6]),
        ),
    ]
