from django.conf.urls import patterns, include, url
from lab2.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hotel.views.home', name='home'),
    url(r'^home/', home),
    url(r'^reserve/', reserve),
    url(r'^query/', query),
    url(r'^about/', about),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
