from django.conf.urls import patterns,url
from friend import views

urlpatterns=patterns('',
	url(r'^add_friend/$',views.add_friend,name='add_friend'),
	url(r'^get_friend/$',views.get_friend,name='get_friend'),
	url(r'^accept_friend/$',views.accept_friend,name='accept_friend'),
	url(r'^update_friend/$',views.update_friend,name='update_friend'),
	url(r'^search_friend/$',views.search_friend,name='search_friend'),
	)
