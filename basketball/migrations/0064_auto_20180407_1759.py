# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import basketball.models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0063_auto_20171001_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonper100statline',
            name='plus_minus_rating',
            field=models.DecimalField(max_digits=6, default=0.0, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='player',
            name='image_src',
            field=models.ImageField(upload_to=basketball.models.get_player_upload_path, blank=True, null=True),
        ),
    ]
