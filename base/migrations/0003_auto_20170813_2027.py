# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20170806_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupsetting',
            name='group',
        ),
        migrations.AddField(
            model_name='group',
            name='fga_min',
            field=models.PositiveIntegerField(default=15),
        ),
        migrations.AddField(
            model_name='group',
            name='possession_min',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ManyToManyField(null=True, related_name='admin_groups', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(null=True, related_name='member_groups', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.DeleteModel(
            name='GroupSetting',
        ),
    ]
