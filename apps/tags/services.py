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

# get user's list of autocomplete tags
def get_autocomplete(request, user=None):
	
	# init
	identity = request.user
	autocomplete_tags = settings.DEFAULT_TAGS
	used_tags = get_used_tags(apps.records.models.Record, identity)
	
	# this block of code will handle merging used_tags and the default_tags
	for tag in used_tags:
		is_unique_tag = True
		
		for idx, autocomplete_tag in enumerate(autocomplete_tags):
			if autocomplete_tag['name'].lower() == tag.name.lower():
				is_unique_tag = False
				break
		
		if not is_unique_tag:
			autocomplete_tags.pop(idx)
		
		autocomplete_tags.append({'name': tag.name})
	
	return autocomplete_tags