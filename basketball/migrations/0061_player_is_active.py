# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0060_tablematrix_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
