from django.conf.urls.defaults import *
from apps.accounts import views

urlpatterns = patterns('',
	url(r'^$', views.profile, {'SSL': True}, name='accounts_profile'),
	url(r'^login/$', views.login, name='accounts_login'),
	url(r'^logout/$', views.logout, name='accounts_logout'),
	url(r'^register/$', views.register, name='accounts_register'),
	url(r'^created/$', views.register, name='accounts_created'),
	url(r'^reset/$', views.reset, {'SSL': True}, name='accounts_reset'),
	url(r'^resetconfirmation/(?P<reset_key>.+)$', views.resetconfirmation, {'SSL': True}, name='accounts_resetconfirmation'),
	url(r'^activate/(?P<activation_key>.+)$', views.activate, name='accounts_activate'),
	#url(r'^(?P<user_id>\d+)$', views.profile, name='accounts_profile'),
	url(r'^(?P<username>.+)$', views.profile, name='accounts_profile'),
)
