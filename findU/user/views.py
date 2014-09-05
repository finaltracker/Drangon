# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from user.untils import finalusername
from django.contrib.auth.models import User
from user.models import UserInfo
from django.core.urlresolvers import reverse


def register_mobile(request):
	if request.method=='POST':
		req=json.loads(request.body)
		data={}
		try:
			mobile=req['mobile']
			password=req['password']
			confirmpass=req['confirmpass']
		except KeyError:
			data['status']=14
			data['error']='缺少必要的项'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json') 
		
		if password!=confirmpass:
			data['status']=10
			data['error']='密码前后不一致'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		password=make_password(password)
		username=finalusername()
		user=User(username=username,password=password,is_staff=False,is_active=True,is_superuser=False)
		user.save()
		user=User.objects.get(username)
		userinfo=UserInfo(user=user,mobile=mobile)
		userinfo.save()
		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
	return HttpResponse(status=400)



def autousername():
	time=timezone.now().timestamp()
	username='u'+str(time)
	return username
def finalusername():
	while 1:
		username=autousername()
		try:
			User.objects.get(username)
		except ObjectDoesNotExist:
			break
	return username