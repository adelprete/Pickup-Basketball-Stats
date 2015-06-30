# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0003_auto_20150628_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='statlines_created',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='playbyplay',
            name='assist',
            field=models.CharField(choices=[('ast', 'AST'), ('pot', 'POT')], max_length=30),
        ),
    ]
