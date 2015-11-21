from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from ball.models import Ball
import json
import logging
from utils.pack_json import toJSON
from ball.tasks import ball_track
from django.db.models import Q
from django.utils import timezone

import pytz

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
		ball = Ball(user=my_user)
		ball.duration = duration
		print 'ball_type {0}'.format(ball_type)
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
		ball_track.delay(user=src_user,ball_id=ball.id, duration=duration,
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
		data['ball_status'] = ball.ball_status
		data['current_lng'] = ball.current_lng
		data['current_lat'] = ball.current_lat
		data['begin_date'] = str(ball.date)
		data['end_date'] = str(ball.end_date)
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

		ball_objs = []

		mask = int(mask)
		distance = int(distance)
		lng = float(lng)
		lat = float(lat)

		if mask==1:
			my_user=User.objects.get(username=src_user)

			balls = Ball.objects.filter(Q(current_lng__lt=lng+distance_scale_lng*distance)
				& Q(current_lng__gt=lng-distance_scale_lng*distance)
				& Q(current_lat__lt=lat+distance_scale_lat*distance)
				& Q(current_lat__gt=lat-distance_scale_lat*distance)
				& ~Q(user=my_user)
				& Q(ball_status=0)).order_by('date')

			if balls:
				for ball in balls:
					ball_obj = {}
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)

		elif mask==2:
			my_user=User.objects.get(username=src_user)
			balls = Ball.objects.filter(user=my_user).filter(ball_status=0).order_by('date')

			if balls:
				for ball in balls:
					ball_obj = {}
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['ball_status'] = ball.ball_status
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)

		elif mask==3:
			balls = Ball.objects.filter(Q(current_lng__lt=lng+distance_scale_lng*distance)
				& Q(current_lng__gt=lng-distance_scale_lng*distance)
				& Q(current_lat__lt=lat+distance_scale_lat*distance)
				& Q(current_lat__gt=lat-distance_scale_lat*distance))
				.filter(ball_status=0).order_by('date')

			if balls:
				print 'got.'
				for ball in balls:
					ball_obj = {}
					ball_obj['user'] = ball.user.username
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_objs.append(ball_obj)
			else:
				print 'nothing.'

		else:
			print 'not support!!'

		data['status']=0
		data['moible'] = src_user
		data['balls'] = ball_objs
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def get_all(request):

	data = {}
	if request.method=='POST':
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		since_date=request.POST.get('since_date')
		require_type=request.POST.get('require_type')
		my_user=User.objects.get(username=src_user)

		from datetime import datetime
		if since_date:
			from dateutil.parser import parse
			tz = pytz.timezone('Asia/Shanghai')
			#date_object = datetime.fromtimestamp(float(since_date),tz)
			date_object = parse(since_date)
			date_object = date_object.astimezone(tz)

		else:
			date_object = timezone.now()
			'''
			date_object = datetime.strptime('%d-%d-%d %d:%d:%d'
				%(now.year,now.month,now.day,now.hour,now.minute,now.second), '%Y-%m-%d %H:%M:%S')
			'''

		ball_objs = []

		require_type = int(require_type)
		if require_type == 1:
			balls = Ball.objects.filter(Q(user=my_user)
				&Q(date__lt=date_object)).order_by('date')

			if balls:
				for ball in balls[0:10]:
					ball_obj = {}
					ball_obj['sender'] = ball.user.username
					if ball.catcher:
						ball_obj['catcher'] = ball.catcher.username
					else:
						ball_obj['catcher'] = 'unknown'
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['ball_status'] = ball.ball_status
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_obj['begin_date'] = str(ball.get_date())
					ball_obj['end_date'] = str(ball.get_end_date())
					ball_objs.append(ball_obj)

		elif require_type == 2:
			balls = Ball.objects.filter(Q(catcher=my_user)
				&Q(end_date__lt=date_object)).order_by('date')

			if balls:
				for ball in balls[0:10]:
					ball_obj = {}
					ball_obj['sender'] = ball.user.username
					if ball.catcher:
						ball_obj['catcher'] = ball.catcher.username
					else:
						ball_obj['catcher'] = 'unknown'
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['ball_status'] = ball.ball_status
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_obj['begin_date'] = str(ball.get_date())
					ball_obj['end_date'] = str(ball.get_end_date())
					balls.append(ball_obj)

		elif require_type == 3:
			balls = Ball.objects.filter(Q(user=my_user)|Q(catcher=my_user))\
				.filter(Q(date__lt=date_object)).order_by('date')

			#import pdb; pdb.set_trace()

			if balls:
				for ball in balls[0:10]:
					ball_obj = {}
					ball_obj['sender'] = ball.user.username
					if ball.catcher:
						ball_obj['catcher'] = ball.catcher.username
					else:
						ball_obj['catcher'] = 'unknown'
					ball_obj['ball_id'] = ball.id
					ball_obj['type'] = ball.ball_type
					ball_obj['ball_status'] = ball.ball_status
					ball_obj['content'] = ball.ball_content
					ball_obj['current_lng'] = ball.current_lng
					ball_obj['current_lat'] = ball.current_lat
					ball_obj['begin_date'] = str(ball.get_date())
					ball_obj['end_date'] = str(ball.get_end_date())
					ball_objs.append(ball_obj)
		else:
			print 'not support'

		data['status']=0
		data['moible'] = src_user
		data['balls'] = ball_objs
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')
