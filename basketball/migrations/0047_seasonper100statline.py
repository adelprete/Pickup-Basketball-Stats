# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0046_tablematrix_game_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonPer100Statline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('game_type', models.CharField(choices=[('5v5', '5on5'), ('4v4', '4on4'), ('3v3', '3on3'), ('2v2', '2on2'), ('1v1', '1on1')], max_length=30)),
                ('gp', models.PositiveIntegerField(verbose_name='Games Played', default=0)),
                ('points_to_win', models.CharField(choices=[('11', '11'), ('30', '30'), ('other', 'Other')], default='11', max_length=30)),
                ('points', models.DecimalField(decimal_places=1, max_digits=4)),
                ('dreb', models.DecimalField(decimal_places=1, max_digits=4)),
                ('oreb', models.DecimalField(decimal_places=1, max_digits=4)),
                ('total_rebounds', models.DecimalField(decimal_places=1, max_digits=4)),
                ('asts', models.DecimalField(decimal_places=1, max_digits=4)),
                ('pot_ast', models.DecimalField(decimal_places=1, max_digits=4)),
                ('blk', models.DecimalField(decimal_places=1, max_digits=4)),
                ('stls', models.DecimalField(decimal_places=1, max_digits=4)),
                ('to', models.DecimalField(decimal_places=1, max_digits=4)),
                ('dreb_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('oreb_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('total_rebounds_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('off_rating', models.DecimalField(decimal_places=1, max_digits=4)),
                ('fg_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('threepm_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ts_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('def_rating', models.DecimalField(decimal_places=1, max_digits=4)),
                ('tp_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ast_fgm_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('ast_fga_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('unast_fgm_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('unast_fga_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('pgm_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('pga_pct', models.DecimalField(decimal_places=1, max_digits=4)),
                ('season', models.ForeignKey(on_delete=models.CASCADE, to='basketball.Season')),
            ],
        ),
    ]
