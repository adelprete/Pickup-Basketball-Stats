# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=30)),
                ('team1_score', models.PositiveIntegerField(default=0)),
                ('team2_score', models.PositiveIntegerField(default=0)),
                ('team1_team_rebounds', models.PositiveIntegerField(default=0)),
                ('team2_team_rebounds', models.PositiveIntegerField(default=0)),
                ('youtube_url', models.URLField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='PlayByPlay',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.TimeField()),
                ('primary_play', models.CharField(max_length=30)),
                ('secondary_play', models.CharField(blank=True, max_length=30)),
                ('assist', models.CharField(choices=[('pot', 'POT'), ('ast', 'AST')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('height', models.CharField(blank=True, max_length=30)),
                ('weight', models.CharField(blank=True, max_length=30)),
                ('image_src', models.ImageField(blank=True, null=True, upload_to='player_images/')),
            ],
        ),
        migrations.CreateModel(
            name='StatLine',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fgm', models.PositiveIntegerField(default=0)),
                ('fga', models.PositiveIntegerField(default=0)),
                ('threepm', models.PositiveIntegerField(default=0)),
                ('threepa', models.PositiveIntegerField(default=0)),
                ('dreb', models.PositiveIntegerField(default=0)),
                ('oreb', models.PositiveIntegerField(default=0)),
                ('total_rebounds', models.PositiveIntegerField(default=0)),
                ('asts', models.PositiveIntegerField(default=0)),
                ('pot_ast', models.PositiveIntegerField(default=0)),
                ('blk', models.PositiveIntegerField(default=0)),
                ('ba', models.PositiveIntegerField(default=0)),
                ('stls', models.PositiveIntegerField(default=0)),
                ('to', models.PositiveIntegerField(default=0)),
                ('fd', models.PositiveIntegerField(default=0)),
                ('pf', models.PositiveIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=models.CASCADE, to='basketball.Game')),
                ('player', models.ForeignKey(on_delete=models.CASCADE, to='basketball.Player')),
            ],
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='assist_player',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='+', to='basketball.Player'),
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='game',
            field=models.ForeignKey(on_delete=models.CASCADE, to='basketball.Game'),
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='primary_player',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='primary_plays', to='basketball.Player'),
        ),
        migrations.AddField(
            model_name='playbyplay',
            name='secondary_player',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='secondary_plays', to='basketball.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='team1',
            field=models.ManyToManyField(to='basketball.Player', related_name='+'),
        ),
        migrations.AddField(
            model_name='game',
            name='team2',
            field=models.ManyToManyField(to='basketball.Player', related_name='+'),
        ),
    ]
