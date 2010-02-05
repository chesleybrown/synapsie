from django.conf.urls.defaults import *
from taglife.apps.tags import views

urlpatterns = patterns('',
	url(r'^$', views.list_tags, name='tag_list'),
	url(r'^create/$', views.add_tag, name='tag_add'),
	url(r'^show/(?P<tag_id>\d+)$', views.show_tag, name='tag_show'),
	url(r'^edit/(?P<tag_id>\d+)$', views.edit_tag, name='tag_edit'),
	url(r'^delete/(?P<tag_id>\d+)$', views.delete_tag, name='tag_delete'),
)
