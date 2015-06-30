from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from feed.models import PosInfo
import time
from django.utils import timezone
import json
import logging
from friend.models import Friend
from utils.pack_jpush import jpush_send_message
from utils.pack_json import toJSON
 
# delta set as : half hour
threshold = 0.5

def locate_update(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('src_user')
		target_user=request.POST.get('target_user')

		user=User.objects.get(username=target_user)		
		target_pos=PosInfo(user=user)
		delta = (timezone.now() - target_pos.date).hours
		if delta < threshold:
			data['status']=0
			data['moible'] = src_user
			data['friend_mobile'] = target_user
			data['lat'] = target_pos.lat
			data['lng'] = target_pos.lng
			return HttpResponse(toJSON(data),content_type='application/json')
		else:
			jpush_send_message(src_user,target_user,303)
			data['status']=401
			return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_get_all(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('src_user')
		target_user=request.POST.get('target_user')

		my_user=User.objects.get(username=target_user)
		friends = Friend.objects.filter(user=my_user)
		all_friends = []
		for relative_friend in friends:
			target_pos=PosInfo(user=relative_friend.friend)
			relative = {}
			relative['friend_mobile'] = relative_friend.friend.username
			relative['lat'] = target_pos.lat
			relative['lng'] = target_pos.lng
			all_friends.append(relative)

		data['status']=0
		data['moible'] = src_user
		data['geo'] = all_freinds
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_upload(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		user_name=request.POST.get('mobile')
		lant=request.POST.get('lant')
		longt=request.POST.get('longt')

		user=User.objects.get(username=user_name)
		
		posinfo=PosInfo(user=user)
		posinfo.lat = lant
		posintof.lng = longt
		posinfo.save()
		data['status']=0
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')
