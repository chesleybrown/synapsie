from datetime import datetime
import random

from django.db.models import Q

import apps.suggestions.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


# get the next suggestion for given user
def get_next_suggestion(request, user=None, skipped_suggestion_id=None):
	
	# init
	identity = request.user
	next_suggestion = None
	user_suggestions = None
	user_suggestion_ids = list()
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get current user_suggestions that are marked completed or ignored
	user_suggestions = (
		apps.suggestions.models.UserSuggestions.objects.all()
		.filter(Q(ignored=True) | Q(completed=True), user=user)
	)
	
	for user_suggestion in user_suggestions:
		user_suggestion_ids.append(user_suggestion.id)
	
	# get a random suggestion that the user hasn't already completed or ignored
	# we have to determine a random suggestion to select like this because MySQL random order sucks
	num_suggestions = apps.suggestions.models.Suggestion.objects.count()
	random_id_range = random.randint(1, num_suggestions)
	
	suggestions = (
		apps.suggestions.models.Suggestion.objects
		.exclude(pk__in=user_suggestion_ids)
		.filter(pk__gte=random_id_range) # trying gte
	)
	
	# if skipped_suggestion_id provided, make sure we don't return that suggestion
	if skipped_suggestion_id is not None:
		suggestions = suggestions.exclude(id=skipped_suggestion_id)
	
	# get one
	suggestions = suggestions.order_by('id')[:1]
	
	# get the first suggestion
	for suggestion in suggestions:
		next_suggestion = suggestion
	
	
	
	
	# if we still don't have a suggestion, try lte... if no match after that, then nothing to suggest
	suggestions = (
		apps.suggestions.models.Suggestion.objects
		.exclude(pk__in=user_suggestion_ids)
		.filter(pk__lte=random_id_range) # trying lte
	)
	
	# if skipped_suggestion_id provided, make sure we don't return that suggestion
	if skipped_suggestion_id is not None:
		suggestions = suggestions.exclude(id=skipped_suggestion_id)
	
	# get the first suggestion
	for suggestion in suggestions:
		next_suggestion = suggestion
	
	return next_suggestion