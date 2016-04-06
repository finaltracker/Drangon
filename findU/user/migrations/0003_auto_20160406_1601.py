# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20160405_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='desc',
            field=models.CharField(max_length=140, blank=True),
            preserve_default=True,
        ),
    ]
