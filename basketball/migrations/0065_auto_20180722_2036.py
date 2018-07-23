# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0064_auto_20180407_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(help_text='Date player received award')),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='AwardCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='category',
            field=models.ForeignKey(to='basketball.AwardCategory'),
        ),
        migrations.AddField(
            model_name='award',
            name='player',
            field=models.ForeignKey(to='basketball.Player'),
        ),
    ]
