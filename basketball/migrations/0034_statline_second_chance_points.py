# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0033_auto_20160229_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='second_chance_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
