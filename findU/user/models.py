# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#用户信息表
class UserInfo(models.Model):
	user=models.OneToOneField(User)
	mobile=models.CharField(max_length=11,blank=True)

