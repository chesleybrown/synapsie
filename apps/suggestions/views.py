from types import *
import sys, pprint
import apps.session_messages as SessionMessages

from apps.suggestions.messages import SuggestionMessages

from apps.tags.utils import get_used_tags, get_popular_tags
from apps.suggestions import services as SuggestionService
from tagging.models import Tag, TaggedItem
from tagging.utils import get_tag_list

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list

@login_required
def setup_suggestions(request):
	
	# init
	messages = SuggestionMessages()
	identity = request.user
	
	# not allowed
	if not identity.is_superuser:
		
		# message
		SessionMessages.create_message(request, messages.get('permission_denied'))
		
	# allowed
	else:
		
		suggestions_tags = {
			1: "school,graduated,great",
			2: "awesome,cars,driving",
			3: "move,great,happy",
			4: "awesome,financial,mortgage",
			5: "friends",
			6: "kist,first",
			7: "anniversary",
			8: "birthday,born",
			9: "drinking,alcohol,friends,first",
			10: "cars,first,financial",
			11: "financial,cars",
			12: "vacation",
			13: "concert,music",
			14: "friends",
			15: "job,first",
			16: "sick,first",
			17: "talent,fun",
			18: "first",
			19: "friends,social,facebook",
			20: "girlfriend,first",
			21: "drinking,alcohol,keg,friends",
			22: "financial,mortgage",
			23: "movies,favorite",
			24: "halloween",
			25: "christmas,family",
			26: "birthday",
			27: "snow,snowboarding,first",
			28: "april fool's",
			29: "games,financial",
			30: "date",
			31: "painful,hospital",
			32: "business,financial",
			33: "financial",
			34: "christmas",
			35: "parents,marriage",
			36: "snowboarding,fun",
			37: "food,favorite",
			38: "thanksgiving",
		}
		
		for key, tags in suggestions_tags.items():
			sug = SuggestionService.get_one(request, suggestion_id=key)
			Tag.objects.update_tags(sug, tags)
		
		# message
		SessionMessages.create_message(request, messages.get('setup_completed'))
	
	return HttpResponseRedirect(reverse('record_index'))