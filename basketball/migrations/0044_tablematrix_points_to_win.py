# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0043_auto_20160511_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablematrix',
            name='points_to_win',
            field=models.CharField(default='11', max_length=30, choices=[('11', '11'), ('30', '30'), ('other', 'Other')]),
        ),
    ]
