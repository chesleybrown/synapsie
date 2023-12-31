from __future__ import division
from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.contenttypes.models import ContentType

from apps.accounts import services as AccountService
from apps.accounts.models import RegistrationProfile

from apps.records.models import Record
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


class RecordService():
	
	# just getting one record
	def get_one(self, request, record_id, tags=False, page=1, user=None, public=False, text=None):
		
		# init
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
	def get_multiple(self, request, tags=False, page=1, user=None, public=False, text=None, results_per_page=25):
		
		# init
		identity = request.user
		records_paginator = None
		
		# no user provided, just use identity
		if not user:
			user = identity
		
		# get user records
		record_list = Record.objects.filter(user=user).order_by('-happened', '-id')
		
		
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
		
		# If page request is in range
		try:
			records_paginator = paginator.page(page)
			records_paginator = self.populate_record_tags(request, records_paginator)
			
		except (EmptyPage, InvalidPage):
			records_paginator = None
		
		return records_paginator
		
	# get friend's shared records
	def get_friends_records(self, request, user=None, page=1, results_per_page=25):
		
		# init
		identity = request.user
		records_paginator = None
		friends = None
		friend_user_ids = list()
		
		# no user provided, just use identity
		if not user:
			user = identity
		
		# get any friends the user has
		friends = AccountService.get_friends(request, user=user, include_self=False)
		
		# if user has friends
		if friends:
			
			# generate list of user_ids
			for friend in friends:
				friend_user_ids.append(friend.user.id)
			
			# get friend PUBLIC records
			record_list = (
				Record.objects.all()
				.select_related('user')
				.filter(user__in=friend_user_ids)
				.filter(personal=0) # only get public
				.order_by('-happened', '-id')
			)
			
			# number of items per page
			paginator = Paginator(record_list, results_per_page)
			
			# If page request is out of range, deliver last page of results.
			try:
				records_paginator = paginator.page(page)
				records_paginator = self.populate_record_tags(request, records_paginator)
				
			except (EmptyPage, InvalidPage):
				records_paginator = None
		
		return records_paginator
		
	def populate_record_tags(self, request, records_paginator):
		
		# all this will populate each record's tags for rendering in a
		# single query
		record_ids = list()
		for record in records_paginator.object_list:
			record_ids.append(record.id)
		
		# get all the current record tags in one query
		record_content_type = ContentType.objects.get_for_model(Record)
		tagged_items = TaggedItem.objects.select_related('tag').filter(object_id__in=record_ids, content_type=record_content_type)
		
		record_map = {}
		for tagged_item in tagged_items:
			record_map[tagged_item.object_id] = list()
		
		for tagged_item in tagged_items:
			record_map[tagged_item.object_id].append(tagged_item.tag)
		
		for record_map_item in record_map:
			#records_paginator.object_list[record_map_item] = record_map[record_map_item]
			for record in records_paginator.object_list:
				if record.id == record_map_item:
					record.tags = record_map[record_map_item]
		# end
		
		return records_paginator
	
	
	# get count of unviewed friend shared records
	def get_unviewed_friend_count(self, request, user=None):
		
		# init
		identity = request.user
		user_registration_profile = None
		friends = None
		friend_user_ids = list()
		count = 0
		
		# no user provided, just use identity
		if not user:
			user = identity
		
		# get user registration profile
		try:
			user_registration_profile = RegistrationProfile.objects.get(user=user)
			
		# weird...
		except RegistrationProfile.DoesNotExist:
			user_registration_profile = None
		
		# get any friends the user has
		friends = AccountService.get_friends(request, user=user, include_self=False)
		
		# if user has friends
		if friends:
			
			# generate list of user_ids
			for friend in friends:
				friend_user_ids.append(friend.user.id)
			
			# get friend PUBLIC records
			record_list = (
				Record.objects.all()
				.select_related('user')
				.filter(user__in=friend_user_ids)
				.filter(personal=0) # only get public
			)
			
			if user_registration_profile.last_viewed_friends_shared:
				record_list = record_list.filter(created__gt=user_registration_profile.last_viewed_friends_shared)
			
			count = record_list.count()
			
		
		return count