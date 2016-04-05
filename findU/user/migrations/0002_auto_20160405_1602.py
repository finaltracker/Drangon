# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='desc',
            field=models.CharField(default=datetime.datetime(2016, 4, 5, 8, 2, 52, 790056, tzinfo=utc), max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='die_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='life_value',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='reward',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='tempo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
