# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0027_statline_ast_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='statline',
            name='ast_fga',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statline',
            name='unast_fga',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
