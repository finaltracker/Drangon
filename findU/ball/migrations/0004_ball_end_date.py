# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ball', '0003_auto_20151022_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='ball',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 8, 26, 21, 468304, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
