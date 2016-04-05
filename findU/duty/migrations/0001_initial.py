# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ball', '0001_initial'),
        ('user', '0002_auto_20160405_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('damage', models.IntegerField(default=0)),
                ('last_point', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ball', models.ForeignKey(related_name='weapon', to='ball.Ball')),
                ('boss', models.ForeignKey(to='user.UserInfo')),
                ('user', models.ForeignKey(related_name='parter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
