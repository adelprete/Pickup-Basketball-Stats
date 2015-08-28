# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0021_auto_20150826_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ['-start_date']},
        ),
        migrations.AlterField(
            model_name='game',
            name='team1_score',
            field=models.PositiveIntegerField(default=0, help_text='Leave 0 if entering plays'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team2_score',
            field=models.PositiveIntegerField(default=0, help_text='Leave 0 if entering plays'),
        ),
    ]
