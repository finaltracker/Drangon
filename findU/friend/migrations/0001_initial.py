# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=200)),
                ('comment', models.CharField(max_length=200)),
                ('verify_status', models.IntegerField(default=0)),
                ('version_id', models.IntegerField(default=0)),
                ('reserved', models.CharField(max_length=140, null=True)),
                ('friend', models.ForeignKey(related_name='friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
