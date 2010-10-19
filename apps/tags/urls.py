from django.conf.urls.defaults import *
from apps.tags import views

urlpatterns = patterns('',
	url(r'^$', views.index_tags, name='tag_index'),
	url(r'^create/$', views.add_tag, name='tag_add'),
	url(r'^show/(?P<tag_id>\d+)$', views.show_tag, name='tag_show'),
	url(r'^edit/(?P<tag_id>\d+)$', views.edit_tag, name='tag_edit'),
	url(r'^delete/(?P<tag_id>\d+)$', views.delete_tag, name='tag_delete'),
)
