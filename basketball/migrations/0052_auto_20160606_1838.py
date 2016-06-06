# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0051_auto_20160606_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasonper100statline',
            name='ast_fga_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='ast_fgm_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='asts',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='blk',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='def_rating',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='dreb',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='dreb_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='fgm_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='off_rating',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='oreb',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='oreb_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='pga_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='pgm_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='points',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='pot_ast',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='stls',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='threepm_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='to',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='total_rebounds',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='tp_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='treb_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='ts_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='unast_fga_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
        migrations.AlterField(
            model_name='seasonper100statline',
            name='unast_fgm_percent',
            field=models.DecimalField(decimal_places=1, max_digits=4, default=0.0),
        ),
    ]
