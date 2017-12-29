# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20171225_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberinvite',
            name='permission',
            field=models.CharField(max_length=30, choices=[('read', 'Read'), ('edit', 'Edit'), ('admin', 'Admin')], null=True),
        ),
    ]
