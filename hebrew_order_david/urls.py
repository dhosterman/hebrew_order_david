from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonner_poll.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'application.views.new'),
    url(r'^application/', include('application.urls')),
    url(r'^accounts/', include('accounts.urls'))
)
