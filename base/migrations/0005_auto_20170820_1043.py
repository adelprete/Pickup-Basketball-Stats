# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_memberprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='possession_min',
            new_name='possessions_min',
        ),
    ]
