from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from apps.about import views

urlpatterns = patterns('django.views.generic.simple',
	url(r'^$', views.root, name='root'),
	url(r'^xd_receiver\.htm$', views.xd_receiver, name='xd_receiver'),
	url(r'^home/$', views.home, name='home'),
	url(r'^about/$', views.about, name="about"),
	url(r'^terms/$', views.terms, name="terms"),
	url(r'^privacy/$', views.privacy, name="privacy"),
	url(r'^acceptableuse/$', views.acceptableuse, name="acceptableuse"),
	url(r'^copyright/$', views.copyright, name="copyright"),
	url(r'^browsers/$', 'direct_to_template', {'template': 'about/browsers.html'}),
)
