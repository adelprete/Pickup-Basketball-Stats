# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0026_auto_20151013_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='ast_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
