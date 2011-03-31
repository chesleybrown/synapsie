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
				'name': friend_lowered,
				'facebook_id': friend['id'],
			})
	
	return autocomplete_tags
	