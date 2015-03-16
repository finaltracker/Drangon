from django.conf.urls import patterns,url
from tips import views

urlpatterns=patterns('',
	url(r'^send_tip/$',views.send_tip,name='send_tip'),
	url(r'^get_tip/$',views.get_tip,name='get_tip'),
	)
