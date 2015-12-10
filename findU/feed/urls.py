from django.conf.urls import patterns,url
from feed import views

urlpatterns=patterns('',
	url(r'^locate_get/$',views.locate_get,name='locate_get'),
	url(r'^locate_upload/$',views.locate_upload,name='locate_upload'),
	url(r'^robot_scan/$',views.robot_scan,name='robot_scan'),
	url(r'^all_position/$',views.all_position,name='all_position'),
	)
