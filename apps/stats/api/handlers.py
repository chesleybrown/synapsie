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

class AnonymousStatHandler(AnonymousBaseHandler):
	allowed_methods = ('GET')

class StatHandler(BaseHandler):
	anonymous = AnonymousStatHandler
	allowed_methods = ('GET')
	model = Record
	
	def read(self, request, type=None, time=None):
		
		# init
		identity = request.user
		user = identity
		messages = StatMessages()
		message = None
		response = dict(
			message = {},
			data = {},
		)
		weekly = None
		monthly = None
		yearly = None
		record_counts = None
		tag_counts = None
		
		if type == 'weekly':
			
			if time == 'all_time':
				weekly = StatService.get_weekly(request, user=user, all_time=True)
			
			elif time == 'recent':
				weekly = StatService.get_weekly(request, user=user, all_time=False)
			
			# I trust that this service layer returns clean data
			clean_weekly = weekly
			
			message = messages.get('found')
			
			response['data'] = {
				'stats': clean_weekly,
			}
		
		elif type == 'monthly':
			
			if time == 'all_time':
				monthly = StatService.get_monthly(request, user=user, all_time=True)
			
			# I trust that this service layer returns clean data
			clean_monthly = monthly
			
			message = messages.get('found')
			
			response['data'] = {
				'stats': clean_monthly,
			}
		
		elif type == 'yearly':
			
			yearly = StatService.get_yearly(request, user=user)
			
			# I trust that this service layer returns clean data
			clean_yearly = yearly
			
			message = messages.get('found')
			
			response['data'] = {
				'stats': clean_yearly,
			}
		
		elif type == 'record_counts':
			
			record_counts = StatService.get_record_counts(request, user=user)
			
			# I trust that this service layer returns clean data
			clean_record_counts = record_counts
			
			message = messages.get('found')
			
			response['data'] = {
				'stats': clean_record_counts,
			}
		
		elif type == 'tag_counts':
			
			tag_counts = StatService.get_tag_counts(request, user=user)
			
			# I trust that this service layer returns clean data
			clean_tag_counts = tag_counts
			
			message = messages.get('found')
			
			response['data'] = {
				'stats': clean_tag_counts,
			}
		
		# not a valid type
		else:
			message = messages.get('not_found')
		
		response['message'] = message
		
		return response
	