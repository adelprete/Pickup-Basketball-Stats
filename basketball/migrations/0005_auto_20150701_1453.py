# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0004_auto_20150629_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='statlines_created',
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(blank=True, max_length=30, choices=[('pot', 'POT'), ('ast', 'AST')]),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist_player',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='basketball.Player', null=True, related_name='+'),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='secondary_player',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='basketball.Player', null=True, related_name='secondary_plays'),
        ),
    ]
