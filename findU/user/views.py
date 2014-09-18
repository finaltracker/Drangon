# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import time
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from user.models import UserInfo
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)

def register_mobile(request):
	data={}

	if request.method=='POST':
		logger.debug(str(request.POST))
		
		try:
			mobile=request.POST.get('mobile')
			password=request.POST.get('password')
			confirmpass=request.POST.get('confirmpass')
			own_imsi=request.POST.get('imsi')
		except KeyError:
			data['status']=14
			data['error']='missing items'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json') 
		
		if password!=confirmpass:
			data['status']=10
			data['error']='password not correct'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		# password=make_password(password)
		user_name=mobile
		logger.debug("[Register]:"+str(user_name)+" / "+str(password))
		try:
			check_user = User.objects.get(username=user_name)
			data['status']=16
			data['error']='mobile already used'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			try:
				check_user_info = UserInfo.objects.get(imsi=own_imsi)
				data['status']=22
				data['error']='imsi already used'
				return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
			except ObjectDoesNotExist:
				user=User(username=user_name,password=password,is_staff=False,is_active=True,is_superuser=False)
				user.save()
				user=User.objects.get(username=user_name)
				userinfo=UserInfo(user=user)
				userinfo.imsi = own_imsi
				userinfo.save()
				data['status']=0
				return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=404
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')		


def login(request):
	data={}

	if request.method == 'POST':		
		logger.debug(str(request.POST))
		mobile = request.POST.get('mobile' )       
		password = request.POST.get('password')
		# password=make_password(password)
		logger.debug("[Login]:"+str(mobile)+" / "+str(password))

		user = User.objects.filter(username = mobile,password = password)

		if user:
			logger.debug("user is exist!!")
			data['status']=0
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
    
	data['status']=503
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def check_register(request):
	data={}

	if request.method == 'POST':		
		logger.debug(str(request.POST))
		# req=json.loads(request.body)
		my_imsi = request.POST.get('imsi')     
		
		logger.debug("[Check_Register]:"+str(my_imsi))
		try:
			user_info = UserInfo.objects.get(imsi=my_imsi)
		except ObjectDoesNotExist:
			data['status']=503
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		if user_info:
			logger.debug("user is: "+user_info.user.username)
			data['status']=0
			data['username']=user_info.user.username
			data['nickname']=user_info.user.nickname
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=400
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	

"""
def autousername():
	# time=timezone.now().timestamp()
	timestamp=time.time()
	username='u'+str(timestamp)
	return username

def finalusername():
	while 1:
		user_name=autousername()
		logger.debug(str(user_name))
		try:
			User.objects.get(username = user_name)
		except ObjectDoesNotExist:
			break

	return user_name
"""	
