from django.conf.urls.defaults import *
from taglife.apps.accounts import views

urlpatterns = patterns('',
	url(r'^login/$', views.login, name='accounts_login'),
	url(r'^logout/$', views.logout, name='accounts_logout'),
	url(r'^register/$', views.register, name='accounts_register'),
)
