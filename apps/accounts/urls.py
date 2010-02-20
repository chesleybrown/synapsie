from django.conf.urls.defaults import *
from taglife.apps.accounts import views

urlpatterns = patterns('',
	url(r'^$', views.show, name='accounts_show'),
	url(r'^login/$', views.login, name='accounts_login'),
	url(r'^logout/$', views.logout, name='accounts_logout'),
	url(r'^register/$', views.register, name='accounts_register'),
	url(r'^(?P<user_id>\d+)$', views.show, name='accounts_show'),
	url(r'^(?P<username>.+)$', views.show, name='accounts_show'),
)
