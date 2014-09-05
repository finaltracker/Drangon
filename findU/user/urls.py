from django.conf.urls import patterns,url
from user import views

urlpatterns=patterns('',
	url(r'^register/$',views.register_mobile,name='mobile'),
	)