from django.db import models
from django.contrib.auth.models import User
from ball.models import Ball
from django.utils import timezone
import pytz

class BossCopy(models.Model):	
	date = models.DateTimeField(auto_now_add=True)
	lat = models.FloatField(default=0,db_index=True)
	lng = models.FloatField(default=0,db_index=True)
	desc = models.CharField(max_length=140)
	tempo = models.IntegerField(default=0)
	reward = models.IntegerField(default=0)
	life_value = models.IntegerField(default=0)
	die_date = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		self.die_date = timezone.now()
		super(BossCopy, self).save(*args, **kwargs)

class DamageRecord(models.Model):
	boss = models.ForeignKey(BossCopy)	
	user = models.ForeignKey(User,related_name='parter')
	ball = models.ForeignKey(Ball,related_name='weapon')
	damage = models.IntegerField(default=0)
	last_point = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)


