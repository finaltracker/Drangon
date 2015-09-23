from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from ball.models import Ball
import json
import logging
from utils.pack_json import toJSON

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
		
		'''
		start ball running, if ball hit people, notify two side.
		if not but get to end, notify two side.
		'''
		ball_track(user=src_user,duration=duration,
			end_lat=end_lat,end_lng=end_lng,begin_lng=begin_lng,begin_lat=begin_lat)

		my_user=User.objects.get(username=src_user)
		ball = new Ball(user=my_user)
		ball.duration = duration
		ball.ball_type = ball_type
		ball.ball_content = ball_content
		ball.end_lat = end_lat
		ball.end_lng = end_lng
		ball.begin_lat = begin_lat
		ball.begin_lng = begin_lng
		ball.save()

		data['status']=0
		data['moible'] = src_user
		data['ball_id'] = ball.id
		return HttpResponse(toJSON(data),content_type='application/json')

	data['status']=503
	return HttpResponse(toJSON(data),content_type='application/json')

def locate_get(request):
	pass

def get_all(request):
	pass