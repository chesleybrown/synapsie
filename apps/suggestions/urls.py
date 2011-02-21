from django.conf.urls.defaults import *
from apps.suggestions import views

urlpatterns = patterns('',
	url(r'^setup/$', views.setup_suggestions, name='setup_suggestions'),
)
