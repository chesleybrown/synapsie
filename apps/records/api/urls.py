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
	url(r'^(?P<emitter_format>.+)/(?P<record_id>\d+)$', record_handler, name='api-record'),
	url(r'^(?P<emitter_format>.+)$', record_handler, name='api-record'),
)