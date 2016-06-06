# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0048_auto_20160604_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='ast_fga_pct',
            new_name='ast_fga_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='ast_fgm_pct',
            new_name='ast_fgm_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='dreb_pct',
            new_name='dreb_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='fg_pct',
            new_name='fgm_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='oreb_pct',
            new_name='oreb_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='pga_pct',
            new_name='pga_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='pgm_pct',
            new_name='pgm_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='threepm_pct',
            new_name='threepm_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='total_rebounds_pct',
            new_name='tp_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='tp_pct',
            new_name='treb_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='ts_pct',
            new_name='ts_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='unast_fga_pct',
            new_name='unast_fga_percent',
        ),
        migrations.RenameField(
            model_name='seasonper100statline',
            old_name='unast_fgm_pct',
            new_name='unast_fgm_percent',
        ),
    ]
