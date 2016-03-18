from django.db import models
from django.contrib.auth.models import User
from ball.models import Ball
from user.models import UserInfo


class DamageRecord(models.Model):
	boss = models.ForeignKey(UserInfo)	
	user = models.ForeignKey(User,related_name='parter')
	ball = models.ForeignKey(Ball,related_name='weapon')
	damage = models.IntegerField(default=0)
	last_point = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)


