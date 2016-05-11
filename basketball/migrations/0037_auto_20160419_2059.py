# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0036_auto_20160418_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='value',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cell',
            name='column',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cell',
            name='row',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
