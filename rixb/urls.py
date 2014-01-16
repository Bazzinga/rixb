from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from rest_framework.authtoken.views import obtain_auth_token
admin.autodiscover()

from blog.views import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', show_index),
    url(r'^index/$', index_handler),
    url(r'^article/([\w\d_-]+)/$', article_handler),
    url(r'^timeline/$', time_line_handler),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^token-auth/', obtain_auth_token),
)
