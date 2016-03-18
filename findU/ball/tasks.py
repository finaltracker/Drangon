from __future__ import absolute_import
from celery import shared_task
from user.models import UserInfo
from django.contrib.auth.models import User
from friend.models import Friend
from feed.models import PosInfo
from ball.models import Ball
from duty.models import BossCopy, DamageRecord
from utils.pack_jpush import jpush_send_message
from utils.path_calc import distance_on_unit_sphere
import math
import time
from django.db.models import Q

@shared_task
def ball_track(*args, **kwargs):
	user = kwargs['user']
	ball_id = kwargs['ball_id']
	begin_lng = kwargs['begin_lng']
	begin_lat = kwargs['begin_lat']
	end_lng = kwargs['end_lng']
	end_lat = kwargs['end_lat']
	duration = kwargs['duration']

	e = 0.0162
	kilometers = 6373

	#distance = distance_on_unit_sphere(begin_lat,begin_lng,end_lat,end_lng) * kilometers

	# duration is minutes, transform to seconds
	duration = float(duration) / 1000
	print 'duration : %d' %duration

	# avoid division by zero, set duration to 15 second
	if duration == 0.0:
		duration = 15

	x = float(begin_lng)
	y = float(begin_lat)
	'''
	linear equation, not for lng/lat geo
	'''
	x1 = x
	y1 = y
	x2 = float(end_lng)
	y2 = float(end_lat)
	a = (y2 - y1)/(x2-x1)
	b = (y2*x1-y1*x2)/(x1-x2)

	#step = (x2-x1)/0.0162
	if math.fabs(x2-x1) > math.fabs(y2-y1):
		step = (x2-x1)/duration
	else:
		step = (y2-y1)/duration

	print 'a: %f, b: %d, step: %f' %(a,b,step)
	i = 1

	my_user=User.objects.get(username=user)
	friends = Friend.objects.filter(user=my_user).filter(~Q(friend=my_user))
	if(friends):
		#print '{0} friends. aho'.format(friends.length)
		print 'friends aho'
	else:
		print 'no friends. oops'

	ball = Ball.objects.get(pk=ball_id)

	while i <= duration:
		print 'x : %f, y: %f' %(x, y)

		if math.fabs(x2-x1) > math.fabs(y2-y1):
			x += step
			y = a*x+b
		else:
			y += step
			x = (y-b)/a

		i += 1
		time.sleep(1)

		'''
		save the ball location, get the near friend with location
		and do some harm or bless to them
		'''
		ball.current_lng = x
		ball.current_lat = y
		ball.save()

		for friend in friends:
			positions = PosInfo.objects.filter(user=friend.friend)
			if positions:
				position = positions[0]
			else:
				print 'no position.'
			if( x-e <position.lng<x+e and y-e <position.lat < y+e ):
				'''
				got clash and notify the friend and owner
				'''
				print 'clash friend.'
				friend_info = UserInfo.objects.get(user=friend.friend)
				friend_info.score -= 100
				friend_info.save()

				push_data = {}
				push_target = friend_info.imsi

				push_data['sender']=str(user)
				push_data['receiver']=str(friend.friend.username)
				push_data['end_lat']=ball.current_lat
				push_data['end_lng']=ball.current_lng
				push_data['ball_id']=ball_id
				push_data['reward']=300
				push_data['damage']=100
				jpush_send_message(str(push_data),push_target, 283)

				owner_info = UserInfo.objects.get(user=my_user)
				owner_info.score += 300
				owner_info.save()

				push_target = owner_info.imsi			
				jpush_send_message(str(push_data),push_target, 285)

				# task has finished, so return
				ball.catcher = friend.friend
				# hardcode here
				ball.demange_score = 100
				ball.reward_score = 300

				ball.ball_status = 3
				ball.save()
				return

	'''
	if it get the end, notify the owner
	'''
	ball.catcher = my_user
	# hardcode here
	ball.demange_score = 100
	ball.reward_score = 0

	ball.ball_status = 3
	ball.save()

	print 'ball boom.'
	owner_info = UserInfo.objects.get(user=my_user)
	owner_info.score -= 100
	owner_info.save()
	
	push_target = owner_info.imsi
	push_data = {}
	push_data['sender']=str(my_user.username)
	push_data['receiver']=str(my_user.username)
	push_data['end_lat']=end_lat
	push_data['end_lng']=end_lng
	push_data['ball_id']=ball_id
	push_data['reward']=0
	push_data['damage']=100	
	jpush_send_message(str(push_data),push_target, 287)


@shared_task
def ball_launch(*args, **kwargs):
	user = kwargs['user']
	ball_id = kwargs['ball_id']
	begin_lng = kwargs['begin_lng']
	begin_lat = kwargs['begin_lat']
	end_lng = kwargs['end_lng']
	end_lat = kwargs['end_lat']
	duration = kwargs['duration']
	copy = kwargs['copy_id']

	e = 0.0162
	kilometers = 6373

	#distance = distance_on_unit_sphere(begin_lat,begin_lng,end_lat,end_lng) * kilometers

	# duration is minutes, transform to seconds
	duration = float(duration) / 1000
	print 'duration : %d' %duration

	x = float(begin_lng)
	y = float(begin_lat)
	'''
	linear equation, not for lng/lat geo
	'''
	x1 = x
	y1 = y
	x2 = float(end_lng)
	y2 = float(end_lat)
	a = (y2 - y1)/(x2-x1)
	b = (y2*x1-y1*x2)/(x1-x2)

	#step = (x2-x1)/0.0162
	if math.fabs(x2-x1) > math.fabs(y2-y1):
		step = (x2-x1)/duration
	else:
		step = (y2-y1)/duration

	print 'a: %f, b: %d, step: %f' %(a,b,step)
	i = 1

	my_user=User.objects.get(username=user)
	boss = BossCopy.objects.get(pk=copy)
	if(boss):
		print 'boss aho'
	else:
		print 'no boss. oops'

	ball = Ball.objects.get(pk=ball_id)

	while i <= duration:
		print 'x : %f, y: %f' %(x, y)

		if math.fabs(x2-x1) > math.fabs(y2-y1):
			x += step
			y = a*x+b
		else:
			y += step
			x = (y-b)/a

		i += 1
		time.sleep(1)

		'''
		save the ball location, get the near friend with location
		and do some harm or bless to them
		'''
		ball.current_lng = x
		ball.current_lat = y
		ball.save()

		if( x-e <boss.lng<x+e and y-e <boss.lat < y+e ):
			'''
			got clash and update boss status and record damage
			if hit last point, do reward dispatch
			'''
			print 'clash boss.'
			if boss.life_value > 100:
				boss.life_value -= 100
				boss.save()

				damage = DamageRecord(boss=copy, user=my_user, ball=ball, damage=100, last_point=0)
				damage.save()
			else:
				damage_value = boss.life_value
				boss.life_value = 0
				boss.save()

				damage = DamageRecord(boss=copy, user=my_user, ball=ball, damage=damage_value, last_point=1)
				damage.save()

				records = DamageRecord.objects.get(boss=copy)
				for record in records:
					user = record.user
					friend_info = UserInfo.objects.get(user=user)
					push_data = {}
					push_target = friend_info.imsi

					push_data['sender']=str(user)
					push_data['receiver']=str(copy.desc)
					push_data['end_lat']=ball.current_lat
					push_data['end_lng']=ball.current_lng
					push_data['ball_id']=ball_id
					push_data['reward']=300
					push_data['damage']=100
					jpush_send_message(str(push_data),push_target, 286)

			# task has finished, so return
			ball.hitter = copy
			# hardcode here
			ball.demange_score = 100
			ball.reward_score = 300

			ball.ball_status = 3
			ball.save()
			return

	'''
	if it get the end, notify the owner
	'''
	ball.catcher = my_user
	# hardcode here
	ball.demange_score = 100
	ball.reward_score = 0

	ball.ball_status = 3
	ball.save()

	print 'ball boom.'
	owner_info = UserInfo.objects.get(user=my_user)
	owner_info.score -= 100
	owner_info.save()
	
	push_target = owner_info.imsi
	push_data = {}
	push_data['sender']=str(my_user.username)
	push_data['receiver']=str(copy.desc)
	push_data['end_lat']=end_lat
	push_data['end_lng']=end_lng
	push_data['ball_id']=ball_id
	push_data['reward']=0
	push_data['damage']=100	
	jpush_send_message(str(push_data),push_target, 287)
