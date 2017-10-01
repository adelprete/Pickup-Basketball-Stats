# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20171001_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='points_to_win',
            field=models.CharField(choices=[('11', '11'), ('30', '30'), ('other', 'Other')], max_length=30, null=True),
        ),
    ]
