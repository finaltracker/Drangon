from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
	user = models.ForeignKey(User)
	nickname = models.CharField(max_length=200)
	phone_mobile = models.CharField(max_length=200)
	avatar = models.ImageField(upload_to='avatar')
	reserved=models.CharField(max_length=140)
	
	def __unicode__(self):
		return self.phone_mobile