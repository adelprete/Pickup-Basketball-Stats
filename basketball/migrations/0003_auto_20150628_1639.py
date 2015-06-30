# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0002_auto_20150628_1539'),
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
        migrations.AlterField(
            model_name='game',
            name='youtube_url',
            field=models.URLField(max_length=2000, blank=True),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(max_length=30, choices=[('pot', 'POT'), ('ast', 'AST')]),
        ),
    ]
