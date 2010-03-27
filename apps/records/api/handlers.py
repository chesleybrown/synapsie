from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.records.messages import RecordMessages
from apps.records.models import Record
from apps.records.forms import RecordForm, RecordAddTagsForm
from tagging.models import Tag
from tagging.utils import parse_tag_input

class AnonymousRecordHandler(AnonymousBaseHandler):
	model = Record
	allowed_methods = ('GET')
	fields = ('id', 'text')

class RecordHandler(BaseHandler):
	anonymous = AnonymousRecordHandler
	allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
	model = Record
	
	# init our empty response
	empty_response = dict(
		message = {},
		data = {},
	)
	
	def read(self, request, record_id=None, tags=False, page=1, user_id=None, username=None, public=False):
		
		#init
		identity = request.user
		user = identity
		messages = RecordMessages()
		message = False
		records = False
		records_paginator = False
		results_per_page = 25
		clean_records = list()
		response = self.empty_response
		
		if record_id is not None:
			
			try:
				record = Record.objects.get(pk=record_id)
				
				# check if record was found
				if record is None:
					return False
				
				# test permission to view
				if not record.can_view(identity):
					return False
				
			except Record.DoesNotExist:
				return False
			
			return record
		
		else:
			
			# if a user is trying to view another user's public feed
			if user_id is not None:
				try:
					# if a user is provided, get that user's public records instead
					if user_id:
						user = User.objects.get(pk=user_id)
					
					# if a username is provided, get by that instead
					elif username:
						user = User.objects.get(username__iexact=username)
					
				except User.DoesNotExist:
					raise Http404
				
			# get user records
			record_list = Record.objects.all().filter(user=user).order_by('-created', '-id')
			
			# only show public if enabled (added user & identity check for safety)
			if public or user != identity:
				record_list = record_list.filter(personal=0)
			
			# filter by tags if provided
			if (tags):
				selected_tags = parse_tag_input(tags)
				record_list = TaggedItem.objects.get_by_model(record_list, selected_tags)
			
			# number of items per page
			paginator = Paginator(record_list, results_per_page)
			
			# If page request is out of range, deliver last page of results.
			try:
				records_paginator = paginator.page(page)
			except (EmptyPage, InvalidPage):
				records_paginator = None
		
		if records_paginator:
			for record in records_paginator.object_list:
				clean_record = {
					'id': record.id,
					'user_id': record.user_id,
					'text': record.text,
					'personal': record.personal,
					'created': record.created,
					'tags': record.tags
				}
				clean_records.append(clean_record)
		
		# determine message to return based on results remaining
		if (records_paginator is None
			or records_paginator and len(records_paginator.object_list) < results_per_page):
			message = messages.get('no_more')
		else:
			message = messages.get('more')
		
		# return message and record created
		response['message'] = message
		response['data'] = {
			'results_per_page': results_per_page,
			'records': clean_records,
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
		response = self.empty_response
		
		# if user has posted
		if request.method == 'POST':
			
			record_create_formset = RecordForm(request.POST, prefix='record_create')
			arr_tags = request.POST.getlist('record_create-tags[]')
			
			# validate form
			if record_create_formset.is_valid():
				clean = record_create_formset.cleaned_data
				
				# generate datetime stamp
				if clean['datetime_set']:
					datetime_string = clean['date'] + ' ' + clean['hour'] + ':' + clean['minute'] + clean['ampm']
					record_datetime = datetime.fromtimestamp(time.mktime(time.strptime(datetime_string, datetime_format)))
				
				# create record, set user
				record = Record(
					user_id = identity.id,
					text = clean['text'],
					personal = int(clean['personal']),
					created = record_datetime
				)
				
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
					'tags': record.clean_tags,
				}
				
				# set message and record created
				response['message'] = messages.get('created')
				response['data'] = clean_record
			
			else:
				
				# set error message, missing data
				response['message'] = messages.get('missing_data')
			
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
		response = self.empty_response
		
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
				
				# return only what we need to
				clean_record = {
					'id': record.id,
					'user_id': record.user_id,
					'text': record.text,
					'personal': record.personal,
					'created': record.created,
					'tags': record.clean_tags,
				}
				
				# set message and record created
				response['message'] = messages.get('updated_tags')
				response['data'] = clean_record
			
			else:
				
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
				record.created = record_datetime
				
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
					'tags': record.clean_tags,
				}
				
				# set message and record created
				response['message'] = messages.get('updated')
				response['data'] = clean_record
			
			else:
				
				# set error message, missing data
				response['message'] = messages.get('missing_data')
		
		return response
	
	def delete(self, request, record_id):
		
		# init
		identity = request.user
		messages = RecordMessages()
		response = self.empty_response
		
		# get record
		record = Record.objects.get(pk=record_id)
		
		# check if record was found
		if record is None:
			raise Http404
		
		# test permission to delete
		if not record.can_delete(identity):
			SessionMessages.create_message(request, messages.get('permission_denied'))
			return HttpResponseRedirect(reverse('record_index'))
		
		# delete it
		record.delete()
		
		# return delete message
		response['message'] = messages.get('deleted')
		return response