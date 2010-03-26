from django.conf.urls.defaults import *
from taglife.apps.accounts import views

urlpatterns = patterns('',
	url(r'^$', views.profile, name='accounts_profile'),
	url(r'^login/$', views.login, name='accounts_login'),
	url(r'^logout/$', views.logout, name='accounts_logout'),
	url(r'^register/$', views.register, name='accounts_register'),
	#url(r'^(?P<user_id>\d+)$', views.profile, name='accounts_profile'),
	url(r'^(?P<username>.+)$', views.profile, name='accounts_profile'),
)
