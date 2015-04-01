from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'findU.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('user.urls',namespace='user')),
    url(r'^feed/',include('feed.urls',namespace='feed')),
    url(r'^friend/',include('friend.urls',namespace='friend')),
    url(r'^tips/',include('tips.urls',namespace='tips')),
)
