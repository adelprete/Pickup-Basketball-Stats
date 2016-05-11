# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0037_auto_20160419_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='value',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
