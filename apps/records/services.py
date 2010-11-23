from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from apps.records.messages import RecordMessages
from apps.records.models import Record
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


class RecordService():
	
	# just getting one record
	def getOne(self, request, record_id, tags=False, page=1, user=None, public=False, text=None):
		
		#init
		identity = request.user
		records = False
		
		# no user provided, just use identity
		if not user:
			user = identity
		
		# just getting one record
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
	
	# getting more than one record
	def getMultiple(self, request, tags=False, page=1, user=None, public=False, text=None):
		
		#init
		identity = request.user
		records = False
		records_paginator = False
		results_per_page = 25
		
		# no user provided, just use identity
		if not user:
			user = identity
		
		# get user records
		record_list = Record.objects.all().filter(user=user).order_by('-created', '-id')
		
		# only show public if enabled (added user & identity check for safety)
		if public or user != identity:
			record_list = record_list.filter(personal=0)
		
		# query provided
		if text:
			record_list = record_list.filter(text__icontains=text)
		
		# filter by tags if provided
		if tags and len(tags) > 0:
			selected_tags = parse_tag_input(tags)
			record_list = TaggedItem.objects.get_by_model(record_list, selected_tags)
		
		# number of items per page
		paginator = Paginator(record_list, results_per_page)
		
		# If page request is out of range, deliver last page of results.
		try:
			records_paginator = paginator.page(page)
		except (EmptyPage, InvalidPage):
			records_paginator = None
		
		return records_paginator
		