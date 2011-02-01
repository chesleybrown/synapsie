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
from apps.records.services import RecordService
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
	
	def read(self, request, record_id=None, tags=False, page=1, user_id=None, username=None, public=False, text=None):
		
		#init
		identity = request.user
		user = identity
		record_service = RecordService()
		messages = RecordMessages()
		message = False
		records = False
		records_paginator = False
		results_per_page = 25
		clean_records = list()
		clean_tags = list()
		response = self.empty_response
		
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
		
		return response
	
	def delete(self, request, record_id):
		
		# init
		identity = request.user
		messages = RecordMessages()
		response = self.empty_response
		
		return response