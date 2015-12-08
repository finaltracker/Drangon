# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import pytz

#用户信息表
class UserInfo(models.Model):
	user=models.OneToOneField(User)
	# mobile=models.CharField(max_length=11,blank=True)
	nickname=models.CharField(max_length=24,blank=True)
	imsi=models.CharField(max_length=32,blank=True)
	avatar=models.ImageField(upload_to='avatar')
	version_count = models.IntegerField(default=0)
	score = models.IntegerField(default=1000)
	# 1: for robot 2: for animal
	category = models.IntegerField(default=0)
	reserved=models.CharField(max_length=140)

	def avatar_url(self):
		if self.avatar and hasattr(self.avatar, 'url'):
			return self.avatar.url
		else:
			return 'avatar/ic_launcher.png'

class LoginInfo(models.Model):
	user=models.ForeignKey(User)
	date=models.DateTimeField(auto_now_add=True)

	def get_date(self):
		tz = pytz.timezone('Asia/Shanghai')
		self.date = self.date.astimezone(tz)
		return self.date	