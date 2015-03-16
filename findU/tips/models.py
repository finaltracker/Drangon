from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
	user = models.ForeignKey(User)
	receiver = models.ForeignKey(User)
	message = models.CharField(max_length=280)
	create_time = models.CharField(max_length=100)
	photo = models.CharField(max_length=200)
	audoo = models.CharField(max_length=200)

	def __str__(self):
		return self.message

