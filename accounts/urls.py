from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bonner_poll.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', 'accounts.views.login_view'),
    url(r'^logout/$', 'accounts.views.logout_view'),
    url(r'^existing_user/$', 'accounts.views.existing_user')
)
