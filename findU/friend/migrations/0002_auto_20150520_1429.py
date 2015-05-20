# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='phone',
            new_name='nickname',
        ),
    ]
