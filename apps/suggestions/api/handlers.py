from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.suggestions.messages import SuggestionMessages
from apps.suggestions.models import Suggestion
from apps.suggestions.forms import UserSuggestionForm
from apps.suggestions import services as SuggestionService

from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

class AnonymousSuggestionHandler(AnonymousBaseHandler):
	model = Suggestion
	allowed_methods = ('GET', 'PUT')
	fields = ('id', 'text')

class SuggestionHandler(BaseHandler):
	anonymous = AnonymousSuggestionHandler
	allowed_methods = ('GET', 'PUT')
	model = Suggestion
	
	def read(self, request, suggestion_id=None):
		
		#init
		identity = request.user
		user = identity
		messages = SuggestionMessages()
		message = False
		suggestion = None
		clean_suggestion = list()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		# update given suggestion for user
		if suggestion_id is not None:
			
			suggestion = SuggestionService.get_one(request, suggestion_id=suggestion_id)
			
			if suggestion:
				
				# clean the tags
				clean_tags = list()
				for tag in suggestion.tags:
					clean_tag = {
						'id': tag.id,
						'name': tag.name,
					}
					clean_tags.append(clean_tag)
				
				# clean before returning
				clean_suggestion = {
					'id': suggestion.id,
					'text': suggestion.text,
					'tags': clean_tags,
				}
				
				response['message'] = messages.get('found')
				
			else:
				response['message'] = messages.get('not_found')
			
			# returned message with clean suggestion
			response['data'] = {
				'suggestion': clean_suggestion,
			}
		
		return response
	
	def create(self, request):
		
		# init
		identity = request.user
		messages = SuggestionMessages()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		return response
	
	def update(self, request, suggestion_id, get_next=False):
		
		# init
		identity = request.user
		user = identity
		messages = SuggestionMessages()
		message = False
		user_suggestion_edit_formset = UserSuggestionForm(prefix='user_suggestion_edit')
		suggestion = None
		next_suggestion = None
		clean = None
		clean_suggestion = list()
		clean_next_suggestion = None
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		# update given suggestion for user
		if suggestion_id is not None:
			
			user_suggestion_edit_formset = UserSuggestionForm(request.PUT, prefix='user_suggestion_edit')
			
			# validate form
			if user_suggestion_edit_formset.is_valid():
				clean = user_suggestion_edit_formset.cleaned_data
				
				suggestion = SuggestionService.update_user_suggestion(request, user=user, suggestion_id=suggestion_id, data=clean)
				
				if suggestion:
					
					# clean the tags
					clean_tags = list()
					for tag in suggestion.tags:
						clean_tag = {
							'id': tag.id,
							'name': tag.name,
						}
						clean_tags.append(clean_tag)
					
					# clean before returning
					clean_suggestion = {
						'id': suggestion.id,
						'text': suggestion.text,
						'tags': clean_tags,
					}
					
					response['message'] = messages.get('user_suggestion_updated')
					
					# get the next suggestion for the user if requested
					if get_next:
						next_suggestion = SuggestionService.get_next_suggestion(request, user=user, skipped_suggestion_id=suggestion_id)
						
						if next_suggestion:
							
							# clean the tags
							clean_tags = list()
							for tag in next_suggestion.tags:
								clean_tag = {
									'id': tag.id,
									'name': tag.name,
								}
								clean_tags.append(clean_tag)
							
							# clean before returning
							clean_next_suggestion = {
								'id': next_suggestion.id,
								'text': next_suggestion.text,
								'tags': clean_tags,
							}
					
				else:
					response['message'] = messages.get('not_found')
				
			else:
				
				# set error message, missing data
				response['message'] = messages.get('missing_data')
			
			# returned message with clean suggestion
			response['data'] = {
				'suggestion': clean_suggestion,
				'next_suggestion': clean_next_suggestion,
			}
		
		return response
	
	def delete(self, request, suggestion_id):
		
		# init
		identity = request.user
		messages = SuggestionMessages()
		response = dict(
			message = messages.get('unknown_error'),
			data = {},
		)
		
		return response