from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import Friend
from user.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import time
from django.utils import timezone
from django.utils.encoding import smart_unicode
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
		# comment: for identify who that add
		# comment = request.POST.get('comment')

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

def get_remote_friend(request):
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

def get_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		client = request.POST.get('client')
		client_imsi = request.POST.get('imsi')
		mobile_friend_version = request.POST.get('mobile_friend_version')

		client_friends = []
		try:
			client_user = User.objects.get(username=client)
			client_info = UserInfo.objects.get(user=client_user)
			current_version = client_info.version_count
			if(current_version-int(mobile_friend_version) == 0):
				logger.debug("something goes wrong!!")

			if(current_version-int(mobile_friend_version) < 2):
				data["update_type"]=2
				client_friends = Friend.objects.filter(user=client_user).filter(version_id__gt=mobile_friend_version)
			else:
				data['update_type']=1
				client_friends = Friend.objects.all()

			record_list = []
			for friend in client_friends:
				record = {}
				record['group'] = smart_unicode(friend.group)
				record['nickname'] = smart_unicode(friend.nickname)
				#TODO: fix it
				record['avatar'] = ""
				record['mobile'] = smart_unicode(friend.phone_mobile)

				logger.debug("record :"+str(record))
				record_list.append(record)

			data['status']=0
			data['server_friend_version']=current_version
			data['friends']=record_list
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def accept_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		client = request.POST.get('client')
		nok = request.POST.get('nok')
		src_imsi = request.POST.get('imsi')
		try:
			src_user_info = UserInfo.objects.get(imsi = src_imsi)
			src_user = src_user_info.user.username
		except ObjectDoesNotExist:
			data['status']=34
			data['error']='sender user do not exist'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		target_user=request.POST.get('target_user')

		try:
			target = User.objects.get(username=target_user)
			user_info = UserInfo.objects.get(user=target)
			push_target = user_info.imsi

			friend = Friend(user=target,nickname=src_user, avatar=src_user_info.avatar)
			version_number = user_info.version_count + 1
			friend.version_id = version_number
			friend.save()

			user_info.version_count = version_number
			user_info.save()

			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag(push_target)
			)
			push.message = jpush.message(msg_content=202, extras=str(src_user))
			push.platform = jpush.all_
			push.send()
			data['status']=0
			data['server_friend_version']=version_number
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def update_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		client = request.POST.get('client')
		nick_name = request.POST.get('nick_name')
		avatar_url = request.POST.get('avatar_url')
		mobile = request.POST.get('mobile')

		try:
			client_user = User.objects.get(username = client)
			client_user_info = UserInfo.objects.get(user=client_user)
			logger.debug("friend nickname is "+nick_name)
			my_friend = Friend.objects.get(user=client_user,nickname=nick_name)

			# set breakpoint to trace
			#import pdb; pdb.set_trace()
			# TODO: fix it
			#my_friend.avatar.url = avatar_url
			my_friend.phone_mobile = mobile
			current_version = client_user_info.version_count + 1
			my_friend.version_id = current_version
			my_friend.save()

			client_user_info.version_count = current_version
			client_user_info.save()

			data['status']=0
			data['server_friend_version']=current_version
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

def search_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		client = request.POST.get('client')
		search_friend = request.POST.get('search_str')

		try:
			client_user = User.objects.get(username = client)
			result = User.objects.filter(username=search_friend)

			record_list = []
			for friend in result:
				get_friend = UserInfo.objects.get(user=friend)
				record = {}
				#record['group'] = friend.group
				record['group'] = ""
				record['nickname'] = smart_unicode(get_friend.nickname)
				# TODO: fix it
				record['avatar'] = ""
				record['mobile'] = smart_unicode(friend.username)

				record_list.append(record)

			data['status'] = 0
			data['friends'] = record_list
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=0
			data['friends']= []
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
			
		data['status']=55
		data['error']='undefine error'
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')			

