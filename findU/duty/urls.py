from django.conf.urls import patterns,url
from duty import views

urlpatterns=patterns('',
	url(r'^check_out/$',views.check_out,name='check_out'),
	url(r'^copy_enter/$',views.copy_enter,name='copy_enter'),
	url(r'^boss_create/$',views.boss_create,name='boss_create'),	
	)