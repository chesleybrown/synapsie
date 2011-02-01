from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, XMLEmitter
from apps.records.api.handlers import RecordHandler

stat_handler = Resource(StatHandler)
Emitter.register('.json', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.json/', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.xml', XMLEmitter, 'text/xml; charset=utf-8')
Emitter.register('.xml/', XMLEmitter, 'text/xml; charset=utf-8')

urlpatterns = patterns('',
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<type>[\'\w\-\!\@\#\$\%\^\&\*\(\),\s\.]+)$', stat_handler, {
		'SSL': True,
	}, name='api-stat'),
	url(r'^(?P<emitter_format>[\.a-z]+)$', stat_handler, {'SSL': True}, name='api-stat'),
)