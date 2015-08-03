from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import UserInfo
from tips.models import Tip
from django.core.exceptions import ObjectDoesNotExist
import json
import jpush as jpush
from findU.conf import app_key, master_secret
import logging
logger = logging.getLogger(__name__)

def send_tip(request):
	# save tip
	# notify receiver
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		mobile=request.POST.get('mobile')
		friend=request.POST.get('friend_mobile')
		try:
			client = User.objects.get(username=mobile)
			to_friend = User.objects.get(username=friend)
			to_friend_info = UserInfo.objects.get(user=to_friend)
		except ObjectDoesNotExist:
			logger.debug("user or friend do not exist!")
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		
		content=request.POST.get('message')
		create_time=request.POST.get('create_time')
		audio_url=request.POST.get('audio_url')
		photo_url=request.POST.get('photo_url')

		tip = Tip(user=client)
		tip.receiver = friend
		tip.message = content
		tip.create_time = create_time
		photo_name = request.FILES['photo_file']._get_name()
		tip.photo.save(photo_name, request.FILES['photo_file'])
		audio_name = request.FILES['audio_file']._get_name()
		tip.audio.save(audio_name, request.FILES['audio_file'])
		tip.save()
		# retrieve tip id for next to get
		cacheID = tip.id

		push_target = to_friend_info.imsi

		_jpush = jpush.JPush(app_key, master_secret)
		push = _jpush.create_push()
		push.audience = jpush.audience(
			jpush.tag(push_target)
		)
		push_data = {}
		push_data['from'] = mobile
		push_data['id'] = cacheID
		push.message = jpush.message(msg_content=302, extras=json.dumps(push_data,ensure_ascii=False))
		push.platform = jpush.all_
		push.send()

		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')


def get_tip(request):
	# get tip
	data = {}

	if request.method=='POST':		
		logger.debug(str(request.POST))

		mobile=request.POST.get('mobile')
		friend=request.POST.get('friend_mobile')
		mesg_id=request.POST.get('mesg_id')
		logger.debug("friend:" + str(friend))
		logger.debug("mobile:" + str(mobile))
		logger.debug("message id:" + str(mesg_id))

		try:
			#client = User.objects.get(username=mobile)
			to_friend = User.objects.get(username=friend)
		except ObjectDoesNotExist:
			logger.debug("user or friend do not exist!")
			data['status']=28
			data['error']='user have not register'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		try:
			tip = Tip.objects.get(user=to_friend, id=mesg_id)
		except ObjectDoesNotExist:
			logger.debug("message do not exist!")
			data['status']=39
			data['error']='message do not exist'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

		data['status']=0
		data['mobile']=tip.user.username
		data['friend_mobile']=tip.receiver
		data['message']=tip.message
		data['create_time']=tip.create_time
		data['audio_url']=tip.audio_url()
		data['photo_url']=tip.photo_url()
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')	