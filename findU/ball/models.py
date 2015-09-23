from django.db import models
from django.contrib.auth.models import User

class Ball(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	ball_type = models.IntField(default=0)
	ball_content = models.CharField(max_length=140)
	duration = models.IntField(default=0)
	end_lat = models.FloatField(default=0,db_index=True)
	end_lng = models.FloatField(default=0,db_index=True)
	begin_lat = models.FloatField(default=0,db_index=True)
	begin_lng = models.FloatField(default=0,db_index=True)
