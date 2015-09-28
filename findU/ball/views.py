from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from ball.models import Ball
import json
import logging
from utils.pack_json import toJSON
from ball.tasks import ball_track
from django.db.models import Q

logger = logging.getLogger(__name__)

def start(request):
	data = {}
	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		ball_type=request.POST.get('type')
		ball_content=request.POST.get('content')
		duration=request.POST.get('duration')
		end_lng=request.POST.get('end_lng')
		end_lat=request.POST.get('end_lat')
		begin_lng=request.POST.get('begin_lng')
		begin_lat=request.POST.get('begin_lat')
		
		my_user=User.objects.get(username=src_user)
		ball = new Ball(user=my_user)
		ball.duration = duration
		ball.ball_type = ball_type
		ball.ball_content = ball_content
		ball.end_lat = end_lat
		ball.end_lng = end_lng
		ball.current_lat = begin_lat
		ball.current_lng = begin_lng
		ball.save()

		'''
		start ball running, if ball hit people, notify two side.
		if not but get to end, notify two side.
		'''
		ball_track(user=src_user,ball_id=ball.id, duration=duration,
			end_lat=end_lat,end_lng=end_lng,begin_lng=begin_lng,begin_lat=begin_lat)

		data['status']=0
		data['moible'] = src_user
		data['ball_id'] = ball.id
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def current_loc(request):
	data = {}
	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		ball_id=request.POST.get('ball_id')

		ball = Ball.objects.get(pk=ball_id)

		data['status']=0
		data['moible'] = src_user
		data['ball_id'] = ball.id
		data['current_lng'] = ball.current_lng
		data['current_lat'] = ball.current_lat
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_get(request):
	data = {}
	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		mask=request.POST.get('mask')
		lng=request.POST.get('lng')
		lat=request.POST.get('lat')
		distance=request.POST.get('distance')

		distance_scale_lng = 0.0162
		distance_scale_lat = 0.09

		if mask==1:	
			my_user=User.objects.get(username=src_user)

			balls = Ball.objects.filter(Q(current_lng_lt=lng+distance_scale_lng*distance)
				& Q(current_lng_gt=lng-distance_scale_lng*distance)
				& Q(current_lat_lt=lat+distance_scale_lat*distance)
				& Q(current_lat_gt=lat-distance_scale_lat*distance)
				& ~Q(user=my_user))

			if balls:
				ball_objs = []
				for ball in balls:
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)			

		elif mask==2:
			my_user=User.objects.get(username=src_user)
			balls = Ball.objects.filter(user=my_user)

			if balls:
				ball_objs = []
				for ball in balls:
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)
					
		elif mask==3:											
			balls = Ball.objects.filter(Q(current_lng_lt=lng+distance_scale_lng*distance)
				& Q(current_lng_gt=lng-distance_scale_lng*distance)
				& Q(current_lat_lt=lat+distance_scale_lat*distance)
				& Q(current_lat_gt=lat-distance_scale_lat*distance))

			if balls:
				ball_objs = []
				for ball in balls:
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)

		else:
			print 'not support!!'		

		data['status']=0
		data['moible'] = src_user
		data['balls'] = ball_objs
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')