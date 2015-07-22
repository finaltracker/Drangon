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

logger = logging.getLogger(__name__)

def locate_get(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		target_user=request.POST.get('friend_mobile')
		require_type=request.POST.get('requireType')

		if require_type == "all":
			my_user=User.objects.get(username=src_user)
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

		elif require_type == "one":
			user=User.objects.get(username=target_user)		
			target_pos=PosInfo(user=user)
			delta = (timezone.now() - target_pos.date).hours
			if delta < threshold:
				data['status']=0
				data['moible'] = src_user

				all_friends = []

				relative = {}
				relative['friend_mobile'] = target_user
				relative['lat'] = target_pos.lat
				relative['lng'] = target_pos.lng	
				all_friends.append(relative)

				data['geo'] = all_freinds
				return HttpResponse(toJSON(data),content_type='application/json')
			else:
				jpush_send_message(src_user,target_user,303)
				data['status']=401
				return HttpResponse(toJSON(data),content_type='application/json')
		else:
			data['status']=19
			return HttpResponse(toJSON(data),content_type='application/json')		



	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_upload(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		user_name=request.POST.get('mobile')
		lant=request.POST.get('lat')
		longt=request.POST.get('lng')

		user=User.objects.get(username=user_name)
		
		posinfo=PosInfo(user=user)
		posinfo.lat = lant
		posinto.lng = longt
		posinfo.save()
		data['status']=0
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')
