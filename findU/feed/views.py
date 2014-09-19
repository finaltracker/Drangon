from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from feed.models import PosInfo
import time
from django.utils import timezone
import json
import jpush as jpush
import logging
from findU.conf import app_key, master_secret

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
			data['location'] = {
				'lant': target_pos.lat,
				'longt': target_pos.lng,
				'user': target_user,
			}
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		else:
			_jpush = jpush.JPush(app_key, master_secret)
			push = _jpush.create_push()
			push.audience = jpush.audience(
				jpush.tag("tag1", target_user)
			)
			push.message = jpush.message(msg_content="locate", extras=src_user)
			push.platform = jpush.all_
			push.send()
			data['status']=0
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=503
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')


def locate_upload(request):
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		user_name=request.POST.get('username')
		lant=request.POST.get('lant')
		longt=request.POST.get('longt')

		user=User.objects.get(username=user_name)
		
		posinfo=PosInfo(user=user)
		posinfo.lat = lant
		posintof.lng = longt
		posinfo.save()
		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

	data['status']=503
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
