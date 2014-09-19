from django.conf.urls import patterns,url
from friend import views

urlpatterns=patterns('',
	url(r'^add_friend/$',views.add_friend,name='add_friend'),
	url(r'^get_friend/$',views.get_friend,name='get_friend'),
	url(r'^ok_friend/$',views.ok_friend,name='ok_friend'),
	)