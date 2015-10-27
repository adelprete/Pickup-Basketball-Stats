# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0028_auto_20151017_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(related_name='team1_set', to='basketball.Player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(related_name='team2_set', to='basketball.Player'),
        ),
    ]
