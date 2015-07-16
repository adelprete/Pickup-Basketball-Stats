# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0010_auto_20150715_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='off_reb_opp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
