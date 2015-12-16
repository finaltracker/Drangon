from django.conf.urls import patterns,url
from duty import views

urlpatterns=patterns('',
	url(r'^check_out/$',views.check_out,name='check_out'),	
	)