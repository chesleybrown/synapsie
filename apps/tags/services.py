from __future__ import division
from datetime import datetime
import time
import settings

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import lib.facebook as Facebook

import apps.records.models
from tagging.models import Tag, TaggedItem
from tagging.utils import get_tag_list
from apps.tags.utils import get_used_tags, get_popular_tags # needed?

from apps.accounts import services as AccountService

# get user's list of autocomplete tags
def get_autocomplete(request, user=None):
	
	# init
	identity = request.user
	autocomplete_tags = None
	used_tags = get_used_tags(apps.records.models.Record, identity)
	friends = None
	
	# set default tags that everyone gets
	autocomplete_tags = settings.DEFAULT_TAGS
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	friends = AccountService.get_facebook_friends(request, user=user)
	
	# this block of code will handle merging used_tags and the default_tags
	for tag in used_tags:
		is_unique_tag = True
		tag_lowered = tag.name.lower()
		
		for idx, autocomplete_tag in enumerate(autocomplete_tags):
			if autocomplete_tag['name'].lower() == tag_lowered:
				is_unique_tag = False
				break
		
		if not is_unique_tag:
			autocomplete_tags.pop(idx)
		
		autocomplete_tags.append({'name': tag_lowered})
	
	# handles adding facebook friends to autocomplete
	if friends:
		for friend in friends:
			is_unique_tag = True
			friend_lowered = friend['name'].lower()
			
			for idx, autocomplete_tag in enumerate(autocomplete_tags):
				if autocomplete_tag['name'].lower() == friend_lowered:
					is_unique_tag = False
					break
			
			if not is_unique_tag:
				autocomplete_tags.pop(idx)
			
			autocomplete_tags.append({
				'name': 'facebook_id-' + friend['id'],
				'facebook_name': friend_lowered,
				'facebook_id': friend['id'],
			})
	
	return autocomplete_tags
	
def set_facebook_names(request, tags, user=None):
	
	# init
	identity = request.user
	facebook_tags = list()
	facebook_friends = list()
	facebook_id_regex = re.compile(r'(?P<facebook_id>facebook_id-\d+)')
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get the user's facebook friends
	facebook_friends = AccountService.get_facebook_friends(request, user=user)
	
	for tag in tags:
		
		# check if provided tag is a facebook_id
		match = facebook_id_regex.search(tag)
		if match:
			try:
				facebook_tag = Tag.objects.get(name=tag)
			except Tag.DoesNotExist:
				
				facebook_id = match.group('facebook_id')
				facebook_name = ''
				
				# check if the provided facebook_id is one of their facebook friends
				for facebook_friend in facebook_friends:
					if facebook_friend.id == facebook_id:
						facebook_name = facebook_friend.name
				
				facebook_tag = Tag(name=tag, facebook_name=facebook_name, facebook_id=facebook_id)
			
			facebook_tags.append(facebook_tag)
		
	return facebook_tags