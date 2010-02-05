from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Home
	url(r'^$', direct_to_template, {
		"template": "homepage.html",
	}, name="home"),
	
	# API
	(r'^api/records', include('apps.records.api.urls')),
	
	# Normal
	(r'^accounts/', include('apps.accounts.urls')),
	(r'^about/', include('apps.about.urls')),
	(r'^records/', include('apps.records.urls')),
	(r'^tags/', include('apps.tags.urls')),
	
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)

if settings.SERVE_MEDIA:
	urlpatterns += patterns('',
		(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)