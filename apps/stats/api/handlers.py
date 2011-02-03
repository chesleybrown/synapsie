from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.stats.messages import StatMessages
from apps.stats import services as StatService

from apps.records.models import Record
from apps.records.forms import RecordForm, RecordAddTagsForm
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

class AnonymousRecordHandler(AnonymousBaseHandler):
	model = Record
	allowed_methods = ('GET')
	fields = ('id', 'text')

class StatHandler(BaseHandler):
	anonymous = AnonymousRecordHandler
	allowed_methods = ('GET')
	model = Record
	
	# init our empty response
	empty_response = dict(
		message = {},
		data = {},
	)
	
	def read(self, request, type=None, time=None):
		
		# init
		identity = request.user
		user = identity
		messages = StatMessages()
		message = False
		response = self.empty_response
		weekly = False
		monthly = False
		
		if type == 'weekly':
			
			if time == 'all_time':
				weekly = StatService.get_weekly(request, user=user, all_time=True)
			
			elif time == 'recent':
				weekly = StatService.get_weekly(request, user=user, all_time=False)
			
			# I trust that this service layer returns clean data
			clean_weekly = weekly
			
			message = messages.get('found')
			
			response['message'] = message
			response['data'] = {
				'stats': clean_weekly,
			}
		
		elif type == 'monthly':
			
			if time == 'all_time':
				monthly = StatService.get_monthly(request, user=user, all_time=True)
			
			# I trust that this service layer returns clean data
			clean_monthly = monthly
			
			message = messages.get('found')
			
			response['message'] = message
			response['data'] = {
				'stats': clean_monthly,
			}
		
		elif type == 'yearly':
			
			yearly = StatService.get_yearly(request, user=user)
			
			# I trust that this service layer returns clean data
			clean_yearly = yearly
			
			message = messages.get('found')
			
			response['message'] = message
			response['data'] = {
				'stats': clean_yearly,
			}
		
		return response
	