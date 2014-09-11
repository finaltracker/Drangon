from django.db import models
from django.contrib.auth.models import User

class PosInfo(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	lat = models.FloatField(default=0,db_index=True)
	lng = models.FloatField(default=0,db_index=True)
	desc = models.CharField(max_length=140)
