from __future__ import absolute_import
from celery import shared_task
from user.models import UserInfo
from friend.models import Friend
from feed.models import PosInfo
from utils.pack_jpush import jpush_send_message

@shared_task
def ball_track(*args, **kwargs):
	user = kwargs['user']
	begin = [kwargs['begin_lnt'],kwargs['begin_lat']]
	end = [kwargs['end_lng'],kwargs['end_lat']]
	duration = kwargs['duration']

	x = float(begin[0])
	y = float(begin[1])
	'''
	linear equation, not for lng/lat geo
	'''
	x1 = float(begin[0])
	y1 = float(begin[1])
	x2 = float(end[0])
	y2 = float(end[1])
	a = (y2 - y1)/(x2-x1)
	b = (y2*x1-y1*x2)/(x1-x2)

	step = (x2-x1)/0.0162

	print 'a: %f, b: %d, step: %f' %(a,b,step)
	i = 1

	my_user=User.objects.get(username=user)
	friends = Friend.objects.filter(user=my_user)
	if(friends):
		print '{0} friends. aho'.format(friends.length)
	else:
		print 'no friends. oops'

	while i <= duration:
		print 'x : %d, y: %d' %(x, y)
		x += step
		y = a*x+b

		'''
		get the near friend with location
		do some harm or bless to them
		'''
		for friend in friends:
			position = PosInfo.objects.get(user=friend.friend)
			if( x-e <position.lng<x+e and y-e <position.lat < y+e ):
				'''
				got clash and notify the friend and owner
				'''
				friend_info = UserInfo.objects.get(user=friend.friend)
				push_target = friend_info.imsi
				jpush_send_message(str(user),push_target, 283)

				owner_info = UserInfo.objects.get(user=my_user)
				push_target = owner_info.imsi
				jpush_send_message(str(friend.friend.username),push_target, 285)

		i += 1
		time.sleep(1)
	'''
	if it get the end, notify the owner
	'''
	owner_info = UserInfo.objects.get(user=my_user)
	push_target = owner_info.imsi
	jpush_send_message(str(friend.friend.username),push_target, 287)