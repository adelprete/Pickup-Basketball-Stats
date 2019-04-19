# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0035_game_points_to_win'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('row', models.PositiveIntegerField()),
                ('column', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TableMatrix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=30)),
                ('out_of_date', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='cell',
            name='matrix',
            field=models.ForeignKey(on_delete=models.CASCADE, to='basketball.TableMatrix'),
        ),
    ]
