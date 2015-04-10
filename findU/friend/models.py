from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
	user = models.ForeignKey(User)
	nickname = models.CharField(max_length=200)
	group = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	comment = models.CharField(max_length=200)
	avatar=models.ImageField(upload_to='avatar')
	verify_status = models.IntegerField(default=0)
	version_id = models.IntegerField(default=0)
	reserved=models.CharField(max_length=140, null=True)

	def __str__(self):
		return self.phone
