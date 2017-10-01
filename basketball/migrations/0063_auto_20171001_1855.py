# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0062_auto_20171001_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='score_type',
            field=models.CharField(null=True, max_length=30, choices=[('1and2', "1's and 2's"), ('2and3', "2's and 3's")], verbose_name='Shot Values'),
        ),
    ]
