from django.conf.urls import patterns, include, url

from doc.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
#dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'supdoc.views.home', name='home'),
	url(r'^$', home),
	#url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    # url(r'^supdoc/', include('supdoc.foo.urls')),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^ajax/', include('ajax.urls')),
)

urlpatterns += patterns('',
		    url(r'^write_data/$', 'doc.views.ajax_write'),
		    url(r'^fetch_data/$', 'doc.views.ajax_fetch'),
			url(r'^send_msg/$', "doc.views.send_msg"),
			url(r'^get_msg/$', "doc.views.get_msg"),
)
