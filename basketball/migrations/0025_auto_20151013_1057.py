# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0024_auto_20150912_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playbyplay',
            name='time',
            field=models.DurationField(),
        ),
    ]
