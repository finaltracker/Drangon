from django.conf.urls import patterns,url
from feed import views

urlpatterns=patterns('',
	url(r'^locate_get/$',views.locate_get_all,name='locate_get'),
	url(r'^locate_upload/$',views.locate_upload,name='locate_upload'),
	)