# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('possession_min', models.PositiveIntegerField(default=100)),
                ('fga_min', models.PositiveIntegerField(default=15)),
                ('putback_window', models.PositiveIntegerField(default=6)),
                ('fastbreak_window', models.PositiveIntegerField(default=10)),
                ('group', models.OneToOneField(to='base.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='settings',
            name='group',
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
