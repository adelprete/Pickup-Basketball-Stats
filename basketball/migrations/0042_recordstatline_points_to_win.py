# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0041_auto_20160511_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordstatline',
            name='points_to_win',
            field=models.CharField(default='11', choices=[('11', '11'), ('30', '30'), ('other', 'Other')], max_length=30),
        ),
    ]
