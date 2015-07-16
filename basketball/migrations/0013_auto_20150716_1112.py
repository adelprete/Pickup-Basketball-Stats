# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0012_auto_20150715_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='youtube_url',
        ),
        migrations.AddField(
            model_name='game',
            name='youtube_id',
            field=models.CharField(max_length=2000, blank=True, verbose_name='Youtube Video ID'),
        ),
    ]
