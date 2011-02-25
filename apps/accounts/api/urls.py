from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, XMLEmitter
from apps.accounts.api.handlers import AccountHandler

account_handler = Resource(AccountHandler)
Emitter.register('.json', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.json/', JSONEmitter, 'application/json; charset=utf-8')
Emitter.register('.xml', XMLEmitter, 'text/xml; charset=utf-8')
Emitter.register('.xml/', XMLEmitter, 'text/xml; charset=utf-8')

urlpatterns = patterns('',
	url(r'^(?P<emitter_format>[\.a-z]+)$', account_handler, {
		'SSL': True,
	}, name='api-account'),
)