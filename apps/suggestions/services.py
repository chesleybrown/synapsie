from datetime import datetime

from django.db.models import Q

import apps.suggestions.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


# get the next suggestion for given user
def get_next_suggestion(request, user=None):
	
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
	suggestions = (
		apps.suggestions.models.Suggestion.objects
		.exclude(pk__in=user_suggestion_ids)
		.order_by('?')[:1]
	)
	
	# get the first suggestion
	for suggestion in suggestions:
		next_suggestion = suggestion
	
	return next_suggestion