# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0054_auto_20160607_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Publish Game?'),
        ),
    ]
