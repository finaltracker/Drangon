from __future__ import absolute_import

from celery import shared_task


@shared_task
def ball_track(*args, **kwargs):
	begin = [kwargs['begin_lat'],kwargs['begin_lng']]
	end = [kwargs['end_lat'],kwargs['end_lng']]
	duration = kwargs['duration']

	x = float(begin[0])
	y = float(begin[1])
	'''
	linear equation
	'''
	x1 = float(begin[0])
	y1 = float(begin[1])
	x2 = float(end[0])
	y2 = float(end[1])
	a = (y2 - y1)/(x2-x1)
	b = (y2*x1-y1*x2)/(x1-x2)

	step = (x2-x1)/20

	print 'a: %f, b: %d, step: %f' %(a,b,step)
	i = 1
	while i <= duration:
		print 'x : %d, y: %d' %(x, y)
		x += step
		y = a*x+b
		i += 1
		time.sleep(1)