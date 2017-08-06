# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('admin', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='admin_groups')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='member_groups')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('possession_min', models.PositiveIntegerField(default=100)),
                ('fga_min', models.PositiveIntegerField(default=15)),
                ('putback_window', models.PositiveIntegerField(default=6)),
                ('fastbreak_window', models.PositiveIntegerField(default=10)),
                ('group', models.OneToOneField(to='base.Group')),
            ],
        ),
    ]
