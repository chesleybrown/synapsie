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
from apps.suggestions import services as SuggestionService

from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

class AnonymousSuggestionHandler(AnonymousBaseHandler):
	model = Suggestion
	allowed_methods = ('GET')
	fields = ('id', 'text')

class SuggestionHandler(BaseHandler):
	anonymous = AnonymousSuggestionHandler
	allowed_methods = ('GET', 'POST')
	model = Suggestion
	
	def read(self, request, suggestion_id=None, skipped_suggestion_id=None, action=None):
		
		#init
		identity = request.user
		user = identity
		messages = SuggestionMessages()
		message = False
		suggestion = None
		clean_suggestion = list()
		response = dict(
			message = {},
			data = {},
		)
		
		# just getting one suggestion randomly, but skipping one suggestion
		if skipped_suggestion_id is not None and action == 'skip':
			
			suggestion = SuggestionService.get_next_suggestion(request, user=user, skipped_suggestion_id=skipped_suggestion_id)
			
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
				
				message = messages.get('not_found')
				
			else:
				message = messages.get('not_found')
			
			# returned message with clean suggestion
			response['message'] = message
			response['data'] = {
				'suggestion': clean_suggestion,
			}
		
		return response
	
	def create(self, request):
		
		#init
		identity = request.user
		messages = RecordMessages()
		record_create_formset = RecordForm(prefix='record_create')
		now = datetime.now()
		str_tags = ','
		clean = None
		record_datetime = None
		datetime_string = False
		datetime_format = "%Y-%m-%d %I:%M%p"
		response = dict(
			message = {},
			data = {},
		)
			
		return response
	
	def update(self, request, record_id, add_tags=False):
		
		#init
		identity = request.user
		messages = RecordMessages()
		record_edit_formset = RecordForm(prefix='record_edit')
		record_add_tags_formset = RecordAddTagsForm(prefix='record_add_tags')
		now = datetime.now()
		str_tags = ','
		clean = None
		record_datetime = None
		datetime_string = False
		datetime_format = "%Y-%m-%d %I:%M%p"
		response = dict(
			message = {},
			data = {},
		)
		
		# get record
		try:
			record = Record.objects.get(pk=record_id)
			
		except Record.DoesNotExist:
			response['message'] = messages.get('not_found')
			return response
		
		# test permission
		if not record.can_edit(identity):
			response['message'] = messages.get('permission_denied')
			return response
		
		# determine if we are handling a full record edit or just adding tags
		if (add_tags):
			record_add_tags_formset = RecordAddTagsForm(request.PUT, prefix='record_add_tags')
			arr_tags = request.PUT.getlist('record_add_tags-tags[]')
			
			# validate form
			if record_add_tags_formset.is_valid():
				clean = record_add_tags_formset.cleaned_data
				
				# add tags
				str_tags += ",".join(arr_tags)
				Tag.objects.update_tags(record, str_tags)
				
				# save record (this will automatically update quality)
				record.save()
				
				# return only what we need to
				clean_record = {
					'id': record.id,
					'user_id': record.user_id,
					'text': record.text,
					'personal': record.personal,
					'created': record.created,
					'happened': record.happened,
					'tags': record.clean_tags,
				}
				
				# set message and record created
				response['message'] = messages.get('updated_tags')
				response['data'] = clean_record
			
			else:
				response['data'] = record.personal
				# set error message, missing data
				response['message'] = messages.get('missing_data')
		
		# this is a full record edit
		else:
			record_edit_formset = RecordForm(request.PUT, prefix='record_edit')
			arr_tags = request.PUT.getlist('record_edit-tags[]')
			
			# validate form
			if record_edit_formset.is_valid():
				clean = record_edit_formset.cleaned_data
				
				# generate datetime stamp
				if clean['datetime_set']:
					datetime_string = clean['date'] + ' ' + clean['hour'] + ':' + clean['minute'] + clean['ampm']
					record_datetime = datetime.fromtimestamp(time.mktime(time.strptime(datetime_string, datetime_format)))
				
				# update record, set user
				record.text = clean['text']
				record.personal = clean['personal']
				record.happened = record_datetime
				
				# save
				record.save()
				
				# add tags
				str_tags += ",".join(arr_tags)
				Tag.objects.update_tags(record, str_tags)
				
				# return only what we need to
				clean_record = {
					'id': record.id,
					'user_id': record.user_id,
					'text': record.text,
					'personal': record.personal,
					'created': record.created,
					'happened': record.happened,
					'tags': record.clean_tags,
				}
				
				# set message and record created
				response['message'] = messages.get('updated')
				response['data'] = clean_record
			
			else:
				
				# set error message, missing data
				response['message'] = messages.get('missing_data')
		
		return response
	
	def delete(self, request, suggestion_id):
		
		# init
		identity = request.user
		messages = RecordMessages()
		response = dict(
			message = {},
			data = {},
		)
		
		return response