from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import Friend
from user.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import time
from django.utils import timezone
import json
import jpush as jpush
import logging
from findU.conf import app_key, master_secret
import logging
logger = logging.getLogger(__name__)

def add_friend(request):
	data = {}

	if request.method == 'POST':		
		logger.debug(str(request.POST))
		
		src_imsi = request.POST.get('imsi')
		try:
			src_user_info = UserInfo.objects.get(imsi = src_imsi)
			src_user = src_user_info.user.username
		except ObjectDoesNotExist:
			data['status']=34
			data['error']='user do not exist'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		target_user=request.POST.get('target_user')

		try:
			check_user = User.objects.get(username=target_user)
			user_info = UserInfo.objects.get(user=check_user)
			push_target = user_info.imsi

			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag(push_target)
			)
			push.message = jpush.message(msg_content=201, extras=str(src_user))
			push.platform = jpush.all_
			push.send()
			data['status']=0
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def get_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		friend = request.POST.get('friend')

		try:
			friend_user = User.objects.get(username=friend)
			friend_info = UserInfo.objects.get(user=friend_user)
			data['status']=0
			data['username']=friend
			data['nickname']=friend_info.nickname
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')		


def ok_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		nok = request.POST.get('nok')
		src_imsi = request.POST.get('imsi')
		try:
			src_user_info = UserInfo.objects.get(imsi = src_imsi)
			src_user = src_user_info.user.username
		except ObjectDoesNotExist:
			data['status']=34
			data['error']='user do not exist'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		target_user=request.POST.get('target_user')

		try:
			target = User.objects.get(username=target_user)
			user_info = UserInfo.objects.get(user=check_user)
			push_target = user_info.imsi
			
			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag(push_target)
			)
			push.message = jpush.message(msg_content=202, extras=str(src_user))
			push.platform = jpush.all_
			push.send()
			data['status']=0
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')	
