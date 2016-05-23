# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from friend.models import Friend
from user.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import time
from django.utils import timezone
from django.utils.encoding import smart_unicode
from utils.pack_json import toJSON
from utils.pack_jpush import jpush_send_message
import logging
logger = logging.getLogger(__name__)


def add_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)
		try:
			client = User.objects.get(username=mobile)
			user_info = UserInfo.objects.get(user = client)
		except ObjectDoesNotExist:
			data['status']=34
			data['error']='user do not exist'
			return HttpResponse(toJSON(data),content_type='application/json')

		add_friend = request.POST.get('friend_mobile')
		# comment: for identify who that add
		# comment = request.POST.get('comment')

		try:
			add_client = User.objects.get(username=add_friend)
			add_client_info = UserInfo.objects.get(user=add_client)
				
			try:
				check_friend = Friend.objects.get(user=add_client, friend=client)
			
				current_version = user_info.version_count
				logger.debug("friend already add, skip it")

			except ObjectDoesNotExist:

				wait_friend = Friend.objects.create(user=add_client, friend=client)
				current_version = add_client_info.version_count + 1

				try:
					have_already_friend = Friend.objects.get(user=client, friend=add_client)

					wait_friend.verify_status = 1
					wait_friend.group = u'我的好友'

				except ObjectDoesNotExist:

					wait_friend.verify_status = 2
					wait_friend.group = u"待验证好友"

					push_target = add_client_info.imsi
					logger.debug("[PUSH]src mobile : "+str(mobile)+push_target)
					jpush_send_message(str(mobile),push_target, 202)

				wait_friend.version_id = current_version
				wait_friend.save()

				add_client_info.version_count = current_version
				add_client_info.save()

			data['status']=0
			data['server_friend_version'] = current_version
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(toJSON(data),content_type='application/json')

def get_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)
		mobile_friend_version = request.POST.get('local_friend_version')

		client_friends = []
		try:
			client = User.objects.get(username=mobile)
			user_info = UserInfo.objects.get(user=client)

			current_version = user_info.version_count
			if(current_version-int(mobile_friend_version) == 0):
				logger.debug("something goes wrong!!")

			if(current_version-int(mobile_friend_version) < 2):
				data["update_type"]=2
				client_friends = Friend.objects.filter(user=client).filter(version_id__gt=mobile_friend_version)
			else:
				data['update_type']=1
				client_friends = Friend.objects.filter(user=client)

			#import pdb; pdb.set_trace()
			record_list = []
			if client_friends:
				for friend in client_friends:
					record = {}
					friend_userinfo = UserInfo.objects.get(user=friend.friend)
					record['group'] = smart_unicode(friend.group)
					record['nickname'] = friend_userinfo.nickname
					#TODO: fix it
					record['avatar_url'] = friend_userinfo.avatar_url()
			
					record['mobile'] = friend.friend.username
					record['verifystatus'] = friend.verify_status

					logger.debug("record :"+str(record))
					record_list.append(record)
				data['server_friend_version']=current_version
			else:
				data['server_friend_version'] = -1

			data['status']=0
			data['friends']=record_list
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(toJSON(data),content_type='application/json')

def accept_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)
		nok = request.POST.get('nok')
		
		try:
			client = User.objects.get(username=mobile)
			user_info = UserInfo.objects.get(user = client)
		except ObjectDoesNotExist:
			data['status']=34
			data['error']='sender user do not exist'
			return HttpResponse(toJSON(data),content_type='application/json')

		to_friend = request.POST.get('friend_mobile')

		try:
			to_client = User.objects.get(username=to_friend)
			to_client_info = UserInfo.objects.get(user=to_client)

			friend = Friend.objects.get(user=client,friend=to_client)
			version_number = user_info.version_count + 1
			friend.version_id = version_number
			friend.nickname = to_client_info.nickname
			friend.group = u'我的好友'
			friend.verify_status = 1
			friend.save()

			user_info.version_count = version_number
			user_info.save()

			try:
				has_done_friend = Friend.objects.get(user=to_client,friend=client)
				logger.debug("friend already has, skip it")
				if has_done_friend.verify_status != 1:
					has_done_friend.verify_status = 1
				if has_done_friend.group != u'我的好友':
					has_done_friend.group = u'我的好友'

				to_client_info.version_count += 1
				to_client_info.save()
				
			except ObjectDoesNotExist:
				done_friend = Friend.objects.create(user=to_client,friend=client)
				current_version = to_client_info.version_count+1
				done_friend.version_id = current_version
				done_friend.nickname = user_info.nickname
				done_friend.group = u'我的好友'
				done_friend.verify_status = 1
				done_friend.save()
				to_client_info.version_count = current_version
				to_client_info.save()

				push_target = to_client_info.imsi
				logger.debug("[PUSH]src mobile : "+str(mobile)+push_target)
				jpush_send_message(str(mobile),push_target, 202)

			data['status']=0
			data['server_friend_version']=version_number
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(toJSON(data),content_type='application/json')

def update_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)
		comment = request.POST.get('comment')
		group = request.POST.get('group')
		description = request.POST.get('description')

		try:
			client = User.objects.get(username = mobile)
			user_info = UserInfo.objects.get(user = client)
			update_friend = request.POST.get('friend_mobile')
			update_client = User.objects.get(username = update_friend)

			my_friend = Friend.objects.get(user=client,friend=update_client)

			# set breakpoint to trace
			#import pdb; pdb.set_trace()
		
			my_friend.group = group
			my_friend.comment = comment
			my_friend.reserved = description
			current_version = user_info.version_count + 1
			my_friend.version_id = current_version
			my_friend.save()

			user_info.version_count = current_version
			user_info.save()

			data['status']=0
			data['server_friend_version']=current_version
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(toJSON(data),content_type='application/json')

def delete_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)

		try:
			client = User.objects.get(username = mobile)
			user_info = UserInfo.objects.get(user = client)

			delete_friend = request.POST.get('friend_mobile')
			delete_client = User.objects.get(username = delete_friend)
			my_friend = Friend.objects.get(user=client,friend=delete_client)

			current_version = user_info.version_count + 1
			
			my_friend.delete()

			user_info.version_count = current_version
			user_info.save()

			data['status']=0
			data['server_friend_version']=current_version
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(toJSON(data),content_type='application/json')

def search_friend(request):
	data = {}

	if request.method == 'POST':
		logger.debug(str(request.POST))

		mobile = request.POST.get('mobile')
		logger.debug("src mobile : "+mobile)
		search_friend = request.POST.get('search_str')

		try:
			client = User.objects.get(username = mobile)
			result = User.objects.filter(username=search_friend)

			record_list = []
			for friend in result:
				get_friend = UserInfo.objects.get(user=friend)
				record = {}
				#record['group'] = friend.group
				record['group'] = ""
				record['nickname'] = smart_unicode(get_friend.nickname)
				# TODO: fix it
				record['avatar_url'] = get_friend.avatar_url()
				record['mobile'] = smart_unicode(friend.username)

				record_list.append(record)

			data['status'] = 0
			data['friends'] = record_list
			return HttpResponse(toJSON(data),content_type='application/json')
		except ObjectDoesNotExist:
			data['status']=0
			data['friends']= []
			return HttpResponse(toJSON(data),content_type='application/json')

		data['status']=55
		data['error']='undefine error'
		return HttpResponse(toJSON(data),content_type='application/json')
