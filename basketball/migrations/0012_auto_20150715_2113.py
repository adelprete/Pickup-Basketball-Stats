# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0011_statline_off_reb_opp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statline',
            old_name='def_reb_opp',
            new_name='dreb_opp',
        ),
        migrations.RenameField(
            model_name='statline',
            old_name='off_reb_opp',
            new_name='oreb_opp',
        ),
    ]
