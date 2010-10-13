from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from taglife.apps.about import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^about/$', views.about, name="about"),
	url(r'^terms/$', views.terms, name="terms"),
	url(r'^privacy/$', views.privacy, name="privacy"),
)
