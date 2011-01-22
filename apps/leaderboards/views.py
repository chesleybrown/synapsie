from types import *
import sys, pprint
import datetime
import apps.session_messages as SessionMessages
import settings

from apps.records.models import Record
from apps.tags.utils import get_used_tags, get_popular_tags
from apps.accounts import services as AccountService
from apps.accounts.models import RegistrationManager, RegistrationProfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list

@login_required
def index_leaderboards(request, page=1):
	
	# init
	identity = request.user
	popular_tags_printable = list()
	results_per_page = 25
	page = 1
	base_friends = False
	friend_ids = list()
	all_friends_paginator = False
	fresh_friends_paginator = False
	stale_friends_paginator = False
	no_facebook_connect = False
	today = datetime.date.today()
	
	# get used/popular tags for current user
	used_tags = get_used_tags(Record, identity)
	popular_tags = get_popular_tags(used_tags)
	
	# get list of user's friends
	base_friends = AccountService.get_friends(request, user=identity, include_self=True)
	
	if base_friends:
		
		friends = base_friends.select_related('user__record').order_by('-quality_of_life').distinct()
		
		# all
		all_friends_paginator = Paginator(friends, results_per_page)
		
		# split the list into people who have posted recently and people who haven't
		three_weeks_ago = today - datetime.timedelta(weeks=3)
		
		# fresh
		fresh_friends = friends.filter(user__record__created__gte=three_weeks_ago)
		fresh_friends_paginator = Paginator(fresh_friends, results_per_page)
		
		# stale
		stale_friends = friends.exclude(user__record__created__gte=three_weeks_ago)
		stale_friends_paginator = Paginator(stale_friends, results_per_page)
		
	else:
		no_facebook_connect = True
	
	# render
	return render_to_response('leaderboards/leaderboard_index.html', {
		'used_tags': used_tags,
		'popular_tags': popular_tags,
		'identity': identity,
		'results_per_page': results_per_page,
		'no_facebook_connect': no_facebook_connect,
		'all_friends_paginator': all_friends_paginator,
		'fresh_friends_paginator': fresh_friends_paginator,
		'stale_friends_paginator': stale_friends_paginator,
	}, context_instance=RequestContext(request))
