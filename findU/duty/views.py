from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from duty.models import DamageRecord
from user.models import UserInfo
from utils.pack_json import toJSON

def check_out(request):
    return render(request, 'duty/detail.html')

def boss_create(request):
	mobile = request.POST.get('mobile')
    	password = request.POST.get('password')
    	confirmpass = request.POST.get('confirmpass')
    	imsi = request.POST.get('imsi')
    	nick_name = request.POST.get('nick_name')
	lat = request.POST.get('lat')
	lng = request.POST.get('lng')
	desc = request.POST.get('desc')
	life = request.POST.get('life')
	reward = request.POST.get('reward')

	user=User(username=mobile,password=password,is_staff=False,is_active=True,is_superuser=False)
	user.save()

	boss = UserInfo(user=user,lat=lat, lng=lng, desc=desc, life_value=life, reward=reward)
	boss.imsi = own_imsi
	boss.nickname = nick_name
	boss.category = 3
	boss.save()

def copy_enter(request):
	copy = UserInfo.objects.filter(category=3).latest('date')
	data = {}

	if copy:
		data['status']=0
		data['copy_id']=cpoy.id
		data['lat']=copy.lat
		data['lng'] = copy.lng
		data['desc'] = copy.desc
		data['life'] = copy.life
		data['tempo'] = copy.status
		return HttpResponse(toJSON(data),content_type='application/json')
	else:
		#there is no boss copy in system!!
		data['status']=277
		return HttpResponse(toJSON(data),content_type='application/json')



