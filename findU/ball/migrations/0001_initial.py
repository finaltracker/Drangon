# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ball',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ball_type', models.IntegerField(default=0)),
                ('ball_status', models.IntegerField(default=0)),
                ('ball_content', models.CharField(max_length=140)),
                ('duration', models.IntegerField(default=0)),
                ('end_lat', models.FloatField(default=0, db_index=True)),
                ('end_lng', models.FloatField(default=0, db_index=True)),
                ('current_lat', models.FloatField(default=0, db_index=True)),
                ('current_lng', models.FloatField(default=0, db_index=True)),
                ('demange_score', models.IntegerField(default=0)),
                ('reward_score', models.IntegerField(default=0)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('catcher', models.ForeignKey(related_name='catcher', to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
