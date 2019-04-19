# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20171218_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberInvite',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('group', models.ForeignKey(on_delete=models.CASCADE, to='base.Group')),
            ],
        ),
    ]
