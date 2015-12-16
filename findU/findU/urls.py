from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'findU.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('user.urls',namespace='user')),
    url(r'^feed/',include('feed.urls',namespace='feed')),
    url(r'^ball/',include('ball.urls',namespace='ball')),
    url(r'^friend/',include('friend.urls',namespace='friend')),
    url(r'^tips/',include('tips.urls',namespace='tips')),
    url(r'^duty/',include('duty.urls',namespace='duty')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
