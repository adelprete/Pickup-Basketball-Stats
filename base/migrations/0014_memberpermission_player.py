# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0064_auto_20180407_1759'),
        ('base', '0013_contact_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberpermission',
            name='player',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, null=True, to='basketball.Player'),
        ),
    ]
