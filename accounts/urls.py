from django.conf.urls import patterns, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonner_poll.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', 'accounts.views.login_view'),
    url(r'^logout/$', 'accounts.views.logout_view')
)
