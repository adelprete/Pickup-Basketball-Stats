# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0053_auto_20160606_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailystatline',
            name='def_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailystatline',
            name='off_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recordstatline',
            name='def_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recordstatline',
            name='off_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seasonstatline',
            name='def_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seasonstatline',
            name='off_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='def_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='off_team_pts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
