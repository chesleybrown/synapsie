from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, XMLEmitter
from apps.tags.api.handlers import TagHandler

tag_handler = Resource(TagHandler)
Emitter.register('.json', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.json/', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.xml', XMLEmitter, 'text/xml; charset=utf-8')
Emitter.register('.xml/', XMLEmitter, 'text/xml; charset=utf-8')

urlpatterns = patterns('',
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<tag_name>.+)/(?P<record_id>\d+)$', tag_handler, name='api-tag'),
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<tag_id>\d+)$', tag_handler, name='api-tag'),
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<tag_name>.+)$', tag_handler, name='api-tag'),
	url(r'^(?P<emitter_format>[\.a-z]+)$', tag_handler, name='api-tag'),
)