# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_group_points_to_win'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberPermission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('permission', models.CharField(null=True, choices=[('read', 'Read'), ('edit', 'Edit'), ('admin', 'Admin')], max_length=30)),
                ('group', models.ForeignKey(null=True, on_delete=models.CASCADE, blank=True, to='base.Group')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='group_permissions')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='memberpermission',
            unique_together=set([('group', 'user')]),
        ),
    ]
