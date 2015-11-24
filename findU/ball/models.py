from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

class Ball(models.Model):
	user = models.ForeignKey(User)
	catcher = models.ForeignKey(User, null=True, related_name='catcher')
	#date = models.DateTimeField(auto_now_add=True)
	date = models.DateTimeField(default=timezone.now)
	ball_type = models.IntegerField(default=0)
	ball_status = models.IntegerField(default=0)
	ball_content = models.CharField(max_length=140)
	duration = models.IntegerField(default=0)
	end_lat = models.FloatField(default=0,db_index=True)
	end_lng = models.FloatField(default=0,db_index=True)
	current_lat = models.FloatField(default=0,db_index=True)
	current_lng = models.FloatField(default=0,db_index=True)
	demange_score = models.IntegerField(default=0)
	reward_score = models.IntegerField(default=0)
	#end_date = models.DateTimeField(auto_now=True)
	end_date = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):

		self.end_date = timezone.now()

		super(Ball, self).save(*args, **kwargs)

	def get_date(self):
		tz = pytz.timezone('Asia/Shanghai')
		self.date = self.date.astimezone(tz)
		return self.date

	def get_end_date(self):
		tz = pytz.timezone('Asia/Shanghai')
		self.end_date = self.end_date.astimezone(tz)
		return self.end_date
