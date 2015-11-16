from django.conf.urls import patterns,url
from ball import views

urlpatterns=patterns('',
	url(r'^start/$',views.start,name='start'),
	url(r'^current_loc/$',views.current_loc,name='current_loc'),
	url(r'^locate_get/$',views.locate_get,name='locate_get'),
	url(r'^get_all/$',views.get_all,name='get_all'),
	)
