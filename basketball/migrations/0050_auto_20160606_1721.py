# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0049_auto_20160606_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='value',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
