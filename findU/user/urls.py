from django.conf.urls import patterns,url
from user import views

urlpatterns=patterns('',
	url(r'^register/$',views.register_mobile,name='register'),
	url(r'^register2/$',views.register_robot,name='register robot'),	
	url(r'^login/$',views.login,name='login'),
	url(r'^check_register/$',views.check_register,name='check_register'),
	url(r'^upload_avatar/$',views.upload_avatar,name='upload_avatar'),
	url(r'^download_avatar/$',views.download_avatar,name='download_avatar'),
	url(r'^delete_user/$',views.delete_user,name='delete_user'),
	url(r'^get_score/$',views.get_score,name='get_score'),
	url(r'^update_nickname/$',views.update_nickname,name='update_nickname'),
	url(r'^get_nickname/$',views.get_nickname,name='get_nickname'),
	)