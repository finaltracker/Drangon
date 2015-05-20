from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
	user = models.ForeignKey(User, related_name='owner')
	friend = models.ForeignKey(User, related_name='friend')
	group = models.CharField(max_length=200)
	nickname = models.CharField(max_length=200)
	comment = models.CharField(max_length=200)
	verify_status = models.IntegerField(default=0)
	version_id = models.IntegerField(default=0)
	reserved=models.CharField(max_length=140, null=True)

	def __str__(self):
		return self.phone
