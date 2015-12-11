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
from django.conf import settings
from django.core.urlresolvers import reverse
import logging
import os

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
			nick_name=request.POST.get('nick_name')
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
				userinfo.nickname = nick_name
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
			logger.debug("user login success!!")
			# login reward, prevent frequently login!
			logininfo = LoginInfo(user=user)
			logininfo.save()
			today = timezone.now()
			today = today-timedelta(hours=today.hour, minutes=today.minute, seconds=today.second)
			todaylogin = LoginInfo.objects.filter(user=user).filter(date__gt=today)
			if len(todaylogin)>1:
				logger.debug("skip reward!!")
			else:
				userinfo = UserInfo.objects.get(user=user)
				userinfo.score += 10
				UserInfo.save()

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
			data['nickname']=user_info.nickname
			data['avatar_url']=user_info.avatar_url()
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=400
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')


def upload_avatar(request):
	data={}
	#get image from client
	#save image to media folder
		
	logger.debug("[photo]request all data: "+ str(request))
	if request.method == "POST":
		user_name = request.POST.get('mobile')
		client = User.objects.get(username=user_name)
		user_info = UserInfo.objects.get(user=client)
		print str(request.FILES)
		print str(request.FILES['avatar_url'])
		logger.debug("[photo]request POST: "+ str(request.POST))
		logger.debug("[photo]upload image: "+str(request.FILES))
		save_file(request.FILES['avatar_url'],user_name)
		user_info.avatar.save(user_name, request.FILES['avatar_url'])
		user_info.save()
		data['status'] = 0
		data['avatar_url'] = user_info.avatar_url()
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def save_file(file, user_name, path=''):

	filename = file._get_name()
	logger.debug("[photo]save image: "+filename)

	path = '%s/%s' % (settings.MEDIA_ROOT , str(path)+user_name)
	#delete old file, and create new one
	if os.path.isfile(path):
		print 'delete existed file'
		os.remove(path)
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def download_avatar(request):
	image_name = request.POST.get('avatar_url')
	logger.debug("image name : "+str(image_name))
	if(image_name != None):
		image_data = open('%s/%s' % (settings.MEDIA_ROOT , str(image_name)), "rb").read()
	return HttpResponse(image_data, content_type="image/png")


def delete_user(request):
	data = {}
	if request.method == 'POST':		
		logger.debug(str(request.POST))
		mobile = request.POST.get('mobile' )
		password = request.POST.get('password')
		# check whether mobile is true user or not
		try:
			user = User.objects.get(username = mobile,password = password)
		except ObjectDoesNotExist:
			data['status']=303
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		logger.debug("user check pass")
		
		from feed.models import PosInfo
		user = User.objects.get(username=mobile)
		locations = PosInfo.objects.filter(user=user)
		if locations:
			for location in locations:
				location.delete()
		user.delete()

		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def register_robot(request):
	data={}

	if request.method=='POST':
		logger.debug(str(request.POST))
		
		try:
			mobile=request.POST.get('mobile')
			password=request.POST.get('password')
			confirmpass=request.POST.get('confirmpass')
			own_imsi=request.POST.get('imsi')
			nick_name=request.POST.get('nick_name')
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
				userinfo.nickname = nick_name
				userinfo.category = 1
				userinfo.save()
				data['status']=0
				return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=404
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')	