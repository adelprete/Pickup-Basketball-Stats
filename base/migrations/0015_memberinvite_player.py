# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_memberpermission_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberinvite',
            name='player',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
