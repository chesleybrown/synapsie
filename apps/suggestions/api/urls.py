from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, XMLEmitter
from apps.suggestions.api.handlers import SuggestionHandler

suggestion_handler = Resource(SuggestionHandler)
Emitter.register('.json', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.json/', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.xml', XMLEmitter, 'text/xml; charset=utf-8')
Emitter.register('.xml/', XMLEmitter, 'text/xml; charset=utf-8')

urlpatterns = patterns('',
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<action>skip)/(?P<skipped_suggestion_id>\d+)$', suggestion_handler, {
		'SSL': True,
	}, name='api-suggestion'),
	url(r'^(?P<emitter_format>[\.a-z]+)/(?P<action>complete)/(?P<suggestion_id>\d+)$', suggestion_handler, {
		'SSL': True,
	}, name='api-suggestion'),
	url(r'^(?P<emitter_format>[\.a-z]+)$', suggestion_handler, {
		'SSL': True
	}, name='api-suggestion'),
)