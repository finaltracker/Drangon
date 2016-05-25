from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from feed.models import PosInfo
from user.models import UserInfo
from django.db.models import Q
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

def all_position(request):
	data = {}

	feeds = []
	users = User.objects.exclude(username='root')
	if users:
		for user in users:
			userinfo = UserInfo.objects.get(user=user)
			if userinfo.category == 0:
				feed = PosInfo.objects.filter(user=user)[0]
				posinfo = {}
				posinfo['name'] = user.username
				posinfo['lat'] = feed.lat
				posinfo['lng'] = feed.lng

				feeds.append(posinfo)

	data['status'] = 0
	data['feeds'] = feeds
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_get(request):
	data = {}
	all_friends = []

	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		target_user=request.POST.get('friend_mobile')
		require_type=request.POST.get('require_type')

		if require_type == "all":
			my_user=User.objects.get(username=src_user)
			friends = Friend.objects.filter(user=my_user)
			
			for relative_friend in friends:
				friend_all_pos=PosInfo.objects.filter(user=relative_friend.friend)
				target_pos = friend_all_pos[len(friend_all_pos)-1]
				relative = {}
				relative['friend_mobile'] = relative_friend.friend.username
				relative['lat'] = target_pos.lat
				relative['lng'] = target_pos.lng
				all_friends.append(relative)

			data['status']=0
			data['moible'] = src_user
			data['geo'] = all_friends
			return HttpResponse(toJSON(data),content_type='application/json')

		elif require_type == "one":
			user=User.objects.get(username=target_user)		
			all_pos=PosInfo.objects.filter(user=user)
			#delta = (timezone.now() - target_pos.date).hours
			target_pos = all_pos[len(all_pos)-1]
			delta = 0
			if delta < threshold:
				data['status']=0
				data['moible'] = src_user


				relative = {}
				relative['friend_mobile'] = target_user
				relative['lat'] = target_pos.lat
				relative['lng'] = target_pos.lng	
				all_friends.append(relative)

				data['geo'] = all_friends
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
		posinfo.lng = longt
		posinfo.save()
		data['status']=0
		''' for test
		data['lng'] = posinfo.lng
		data['lat'] = posinfo.lat
		'''
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def robot_scan(request):
	data = {}
	if request.method=='POST':
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		lng=request.POST.get('lng')
		lat=request.POST.get('lat')
		#distance=request.POST.get('distance')

		distance_scale_lng = 0.0162
		distance_scale_lat = 0.09

		robot_objs = []

		# default: 1 mile
		distance = 1000 
		lng = float(lng)
		lat = float(lat)


		my_user=User.objects.get(username=src_user)

		feeds = PosInfo.objects.filter(Q(lng__lt=lng+distance_scale_lng*distance)
			& Q(lng__gt=lng-distance_scale_lng*distance)
			& Q(lat__lt=lat+distance_scale_lat*distance)
			& Q(lat__gt=lat-distance_scale_lat*distance)).order_by('date')

		if feeds:
			print 'get feeds'
			for feed in feeds:
				user = feed.user
				userinfo = UserInfo.objects.get(user=user)
				if userinfo.category > 0:
					robot_obj = {}
					robot_obj['user'] = user.username
					robot_obj['current_lng'] = feed.lng
					robot_obj['current_lat'] = feed.lat
					robot_obj['avatar_url'] = '/media/avatar/ic_launcher.png'
					robot_objs.append(robot_obj)

		else:
			print 'no feeds'

		data['status']=0
		data['moible'] = src_user
		data['robots'] = robot_objs
		return HttpResponse(toJSON(data),content_type='application/json')
