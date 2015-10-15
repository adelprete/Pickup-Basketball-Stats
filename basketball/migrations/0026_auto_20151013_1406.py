# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0025_auto_20151013_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='ast_fgm',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='pga',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='pgm',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='unast_fgm',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
