# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_memberinvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberinvite',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='memberinvite',
            name='creation_date',
            field=models.DateField(null=True, auto_now_add=True),
        ),
    ]
