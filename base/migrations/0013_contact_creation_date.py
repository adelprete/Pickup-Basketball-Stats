# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='creation_date',
            field=models.DateField(null=True, auto_now_add=True),
        ),
    ]
