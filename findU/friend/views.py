from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import Friend
from user.models import UserInfo
import time
from django.utils import timezone
import json
import jpush as jpush
import logging
from findU.conf import app_key, master_secret

def add_friend(request):
	data = {}

	if request.method == 'POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('src_user')
		target_user=request.POST.get('target_user')

		try:
			check_user = User.objects.get(username=target_user)

			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag("tag1", target_user)
			)
			push.message = jpush.message(msg_content="add friend", extras=src_user)
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
		src_user=request.POST.get('src_user')
		target_user=request.POST.get('target_user')

		try:
			target_user = User.objects.get(username=target_user)

			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag("tag1", target_user)
			)
			push.message = jpush.message(msg_content="ok friend", extras=src_user)
			push.platform = jpush.all_
			push.send()
			data['status']=0
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')	