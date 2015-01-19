from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonner_poll.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'application.views.new'),
    url(r'^post/$', 'application.views.post'),
    url(r'^update/$', 'application.views.update'),
    url(r'^show/$', 'application.views.show'),
    url(r'^thank_you/$', 'application.views.thank_you'),
    url(r'^error/$', 'application.views.error'),
    url(r'^export_excel/$', 'application.views.export_as_excel')
)
