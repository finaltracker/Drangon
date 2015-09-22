from django.shortcuts import render

# Create your views here.

def start(request):
	if request.method=='POST':		
		logger.debug(str(request.POST))

		src_user=request.POST.get('mobile')
		ball_type=request.POST.get('type')
		ball_content=request.POST.get('content')
		duration=request.POST.get('duration')
		end_lat=request.POST.get('end_lat')
		end_lng=request.POST.get('end_lng')
		begin_lat=request.POST.get('begin_lat')
		begin_lng=request.POST.get('begin_lng')

		'''
		start ball running, if ball hit people, notify two side.
		if not but get to end, notify two side.
		'''
		ball_track(duration=duration,
			end_lat=end_lat,end_lng=end_lng,begin_lng=begin_lng,begin_lat=begin_lat)