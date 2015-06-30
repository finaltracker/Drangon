from django.conf.urls import patterns,url
from feed import views

urlpatterns=patterns('',
	url(r'^locate_update/$',views.locate_update,name='locate_update'),
	url(r'^locate_get_all/$',views.locate_get_all,name='locate_get_all'),
	url(r'^locate_upload/$',views.locate_upload,name='locate_upload'),
	)