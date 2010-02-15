from django.conf.urls.defaults import *
from taglife.apps.records import views

urlpatterns = patterns('',
	url(r'^$', views.index_records, name='record_index'),
	url(r'^page/(?P<page>\d+)$', views.index_records, name='record_index'),
	url(r'^tags/(?P<tags>.+)$', views.index_records, name='record_index'),
	url(r'^page/(?P<page>\d+)/tags/(?P<tags>.+)$', views.index_records, name='record_index'),
	url(r'^public/(?P<user_id>\d+)$', views.public_records, name='record_public'),
	url(r'^public/(?P<username>.+)$', views.public_records, name='record_public'),
	url(r'^public/$', views.public_records, name='record_public'),
	url(r'^search/$', views.search_records, name='record_search'),
	url(r'^search/(?P<query>.+)$', views.search_records, name='record_search'),
	url(r'^list/$', views.list_records, name='record_list'),
	url(r'^create/$', views.add_record, name='record_add'),
	url(r'^show/(?P<record_id>\d+)$', views.show_record, name='record_show'),
	url(r'^edit/(?P<record_id>\d+)$', views.edit_record, name='record_edit'),
	url(r'^delete/(?P<record_id>\d+)$', views.delete_record, name='record_delete'),
)
