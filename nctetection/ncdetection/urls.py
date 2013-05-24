from django.conf.urls import patterns, include, url
from grouping.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('views',
		#('^girlsmining/$', girlsmining),
		#('^girlsmining/classify/$', classify),
		#('^girlsmining/test/$', test),
		#('^update/$', update),
		#('^find_robots/$', find_robots),
		#('^set_status_info/$', set_status_info),
		('^hello_world/$', hello_world),
		('^hello_world\/_static\/force\/force\.json$', hello_world_force),
    # Examples:
    # url(r'^$', 'girlsMining.views.home', name='home'),
    # url(r'^girlsMining/', include('girlsMining.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
