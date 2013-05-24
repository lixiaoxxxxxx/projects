from django.conf.urls import patterns, include, url
from helloworld.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helloworld.views.home', name='home'),
    # url(r'^helloworld/', include('helloworld.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	url(r'^hello/$', hello),
	url(r'^browser/$', browser),
	url(r'^time/$', time),
	#url(r'^[a-z]*$', hello),
	url(r'^time/plus/(\d{1,2})/$', hours_ahead),
	url(r'^search-form/$', search_form),
	url(r'^search/$', search),
	url(r'^home/$', home),
	url(r'^blog/$', blog),
)
