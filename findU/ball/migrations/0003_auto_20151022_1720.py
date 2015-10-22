# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ball', '0002_ball_ball_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ball',
            name='catcher',
            field=models.ForeignKey(related_name='catcher', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ball',
            name='demange_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ball',
            name='reward_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
