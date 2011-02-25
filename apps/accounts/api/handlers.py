from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.accounts.messages import AccountMessages
from apps.accounts.models import RegistrationProfile
from apps.accounts import services as AccountService

from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

class AnonymousAccountHandler(AnonymousBaseHandler):
	model = RegistrationProfile
	allowed_methods = ('GET')
	fields = ('id', 'text')

class AccountHandler(BaseHandler):
	anonymous = AnonymousAccountHandler
	allowed_methods = ('GET', 'PUT')
	model = RegistrationProfile
	
	def read(self, request):
		
		# init
		identity = request.user
		messages = AccountMessages()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		return response
	
	def create(self, request):
		
		# init
		identity = request.user
		messages = AccountMessages()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		return response
	
	def update(self, request):
		
		# init
		identity = request.user
		user = identity
		messages = AccountMessages()
		message = False
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		default_put = {
			'viewed_friends_shared': False,
		}
		
		# merge with default_put
		put = dict(default_put.items() + request.PUT.items())
		
		# update last_viewed_friends_shared
		if put['viewed_friends_shared']:
			
			user_registration_profile = AccountService.update_last_viewed_friends_shared(user)
			
			# returned message
			response['message'] = messages.get('updated_last_viewed')
			response['data'] = {
			}
		
		return response
	
	def delete(self, request, suggestion_id):
		
		# init
		identity = request.user
		messages = AccountMessages()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		return response