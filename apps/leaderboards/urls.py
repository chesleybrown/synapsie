from django.conf.urls.defaults import *
from apps.leaderboards import views

urlpatterns = patterns('',
	url(r'^$', views.index_leaderboards, {'SSL': True}, name='leaderboard_index'),
	url(r'^page/(?P<page>\d+)$', views.index_leaderboards, {'SSL': True}, name='leaderboard_index'),
)
