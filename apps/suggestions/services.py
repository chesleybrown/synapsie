from datetime import datetime
import random

from django.db.models import Q

import apps.suggestions.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

# just getting one suggestion
def get_one(request, suggestion_id):
	
	# init
	suggestion = None
	
	# get the suggestion
	try:
		suggestion = apps.suggestions.models.Suggestion.objects.get(pk=suggestion_id)
	except apps.suggestions.models.Suggestion.DoesNotExist:
		suggestion = None
		pass
	
	return suggestion

# get the next suggestion for given user
def get_next_suggestion(request, user=None, skipped_suggestion_id=None):
	
	# init
	identity = request.user
	next_suggestion = None
	user_suggestions = None
	user_suggestion_ids = list()
	attempt = 1
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get current user_suggestions that are marked completed or ignored
	user_suggestions = (
		apps.suggestions.models.UserSuggestions.objects.all()
		.filter(Q(ignored=True) | Q(completed=True), user=user)
	)
	
	for user_suggestion in user_suggestions:
		user_suggestion_ids.append(user_suggestion.suggestion_id)
	
	# get a random suggestion that the user hasn't already completed or ignored
	# we have to determine a random suggestion to select like this because MySQL random order sucks
	num_suggestions = apps.suggestions.models.Suggestion.objects.count()
	if num_suggestions > 0:
		random_id_range = random.randint(1, num_suggestions)
		
		# only ever try twice
		while attempt <= 2 and next_suggestion is None:
			
			suggestions = (
				apps.suggestions.models.Suggestion.objects
				.exclude(pk__in=user_suggestion_ids)
			)
			
			# trying greater than or equal to
			if attempt == 1:
				suggestions = suggestions.filter(pk__gte=random_id_range)
				
			# trying less than
			else:
				suggestions = suggestions.filter(pk__lt=random_id_range)
			
			# if skipped_suggestion_id provided, make sure we don't return that suggestion
			if skipped_suggestion_id is not None:
				suggestions = suggestions.exclude(id=skipped_suggestion_id)
			
			# get one
			suggestions = suggestions.order_by('id')[:1]
			
			# get the first suggestion
			for suggestion in suggestions:
				next_suggestion = suggestion
			
			# increment attempt num
			attempt += 1
	
	return next_suggestion
	
# mark a suggestion as completed by given user
def update_user_suggestion(request, user=None, suggestion_id=None, data=None):
	
	# init
	identity = request.user
	suggestion = None
	user_suggestion = None
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get the suggestion the user completed
	try:
		suggestion = apps.suggestions.models.Suggestion.objects.get(pk=suggestion_id)
	except apps.suggestions.models.Suggestion.DoesNotExist:
		suggestion = None
		pass
	
	if suggestion:
		
		# check if the user already has this suggestion (user_suggestion)
		try:
			user_suggestion = apps.suggestions.models.UserSuggestions.objects.get(suggestion=suggestion, user=user)
		except apps.suggestions.models.UserSuggestions.DoesNotExist:
			user_suggestion = None
			pass
		
		# no user_suggestion yet, create one
		if not user_suggestion:
			user_suggestion = apps.suggestions.models.UserSuggestions()
		
		# update what we need to
		user_suggestion.user = user
		user_suggestion.suggestion = suggestion
		
		if 'completed' in data and data['completed'] is not None:
			user_suggestion.completed = data['completed']
		
		if 'ignored' in data and data['ignored'] is not None:
			user_suggestion.ignored = data['ignored']
		
		if 'viewed' in data and data['viewed'] is not None:
			user_suggestion.viewed = data['viewed']
		
		user_suggestion.save()
	
	return suggestion