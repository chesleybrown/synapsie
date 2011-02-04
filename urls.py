from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Home
	#url(r'^$', direct_to_template, {
	#	"template": "homepage.html",
	#}, name="home"),
	
	# Errors
	url(r'^error/404$', direct_to_template, {
		"template": "404.html",
	}, name="404"),
	url(r'^error/500$', direct_to_template, {
		"template": "500.html",
	}, name="500"),
	
	# API
	(r'^api/records', include('apps.records.api.urls')),
	(r'^api/tags', include('apps.tags.api.urls')),
	(r'^api/stats', include('apps.stats.api.urls')),
	
	# Normal
	(r'^', include('apps.about.urls')),
	(r'^accounts/', include('apps.accounts.urls')),
	(r'^records/', include('apps.records.urls')),
	(r'^tags/', include('apps.tags.urls')),
	(r'^leaderboards/', include('apps.leaderboards.urls')),
	#(r'^stats/', include('apps.stats.urls')),
	
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