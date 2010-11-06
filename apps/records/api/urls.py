from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, XMLEmitter
from apps.records.api.handlers import RecordHandler

record_handler = Resource(RecordHandler)
Emitter.register('.json', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.json/', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.xml', XMLEmitter, 'text/xml; charset=utf-8')
Emitter.register('.xml/', XMLEmitter, 'text/xml; charset=utf-8')

urlpatterns = patterns('',
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<record_id>\d+)$', record_handler, {'SSL': True}, name='api-record'),
	url(r'^(?P<emitter_format>[\.a-z]+)/add_tags/(?P<record_id>\d+)$', record_handler, {
		'SSL': True,
		'add_tags': True,
	}, name='api-record-add_tags'),
	url(r'^(?P<emitter_format>[\.a-z]+)/page/(?P<page>\d+)$', record_handler, {'SSL': True}, name='api-record'),
	url(r'^(?P<emitter_format>[\.a-z]+)/public/(?P<user_id>\d+)/page/(?P<page>\d+)$', record_handler, {
		'SSL': True,
		'public': True,
	}, name='api-record_public'),
	
	url(r'^(?P<emitter_format>[\.a-z]+)/page/(?P<page>\d+)/tags/(?P<tags>[\'\w\-\!\@\#\$\%\^\&\*\(\),\s\.]+)/(?P<text>.*)$', record_handler, {'SSL': True}, name='api-record'),
	url(r'^(?P<emitter_format>[\.a-z]+)/page/(?P<page>\d+)/(?P<tags>.{0})/(?P<text>.*)$', record_handler, {'SSL': True}, name='api-record'),
	
	url(r'^(?P<emitter_format>[\.a-z]+)/page/(?P<page>\d+)/(?P<text>.*)$', record_handler, {'SSL': True}, name='api-record'),
	url(r'^(?P<emitter_format>[\.a-z]+)$', record_handler, {'SSL': True}, name='api-record'),
)