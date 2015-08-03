from django.db import models
from django.contrib.auth.models import User

class Tip(models.Model):
	user = models.ForeignKey(User)
	receiver = models.CharField(max_length=200)
	message = models.CharField(max_length=280)
	create_time = models.CharField(max_length=100)
	photo = models.ImageField(upload_to='photo')
	audio = models.FileField(upload_to='audio')

	def __unicode__(self):
		return self.message

	def photo_url(self):
		if self.photo and hasattr(self.photo, 'url'):
			return self.photo.url
		else:
			return ''

	def audio_url(self):
		if self.audio and hasattr(self.audio, 'url'):
			return self.audio.url
		else:
			return ''			