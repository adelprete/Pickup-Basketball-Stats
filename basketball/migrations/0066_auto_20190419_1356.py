# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0065_auto_20180722_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={'ordering': ('-date',)},
        ),
    ]
