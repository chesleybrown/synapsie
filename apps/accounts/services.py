from __future__ import division
from datetime import datetime
import time
import settings

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import lib.facebook as Facebook

import apps.records.models
import apps.accounts.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

# import the logging library
import logging
logger = logging.getLogger('django')


# given a user, get their friends
def get_friends(request, user=None, include_self=False):
	
	# init
	identity = request.user
	friends = None
	friend_facebook_ids = list()
	facebook_friends = False
	debug = False
	debug_ids = (
		597160467, # tiffany
		589794771, # tim
		604615254, # trudel
	)
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	fb_connect = Facebook.FBConnect()
	facebook_user = fb_connect.get_user_from_cookie(request.COOKIES, '168453549861030', '25dd90990d7444d4c8b7a5467ac6bc43')
	
	if facebook_user:
		facebook_graph = Facebook.GraphAPI(facebook_user['access_token'])
		facebook_profile = facebook_graph.get_object('me')
		facebook_friends = facebook_graph.get_connections('me', 'friends')
	
	if facebook_friends and facebook_friends['data']:
		
		# generate list of ids
		friend_facebook_ids.append(facebook_user['uid'])
		for facebook_friend in facebook_friends['data']:
			friend_facebook_ids.append(facebook_friend['id'])
		
		# get user's friends
		friends = apps.accounts.models.RegistrationProfile.objects.select_related('user').filter(facebook_id__in=friend_facebook_ids)
		
		if not include_self:
			friends = friends.exclude(user=user)
	
	if debug:
		friends = apps.accounts.models.RegistrationProfile.objects.select_related('user').filter(facebook_id__in=debug_ids)
	
	return friends
	
def get_facebook_friends(request, user=None):
	
	# init
	identity = request.user
	friends = None
	friend_facebook_ids = list()
	facebook_friends = False
	debug = False
	debug_facebook_friends_data = (
		{
			'name': 'Tiffany White',
			'id': '597160467',
		},
		{
			'name': 'Tim Oram',
			'id': '589794771',
		},
		{
			'name': 'Christopher Trudel',
			'id': '604615254',
		},
		{
			'name': 'Someone Else',
			'id': '10002',
		},
	)
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	fb_connect = Facebook.FBConnect()
	facebook_user = fb_connect.get_user_from_cookie(request.COOKIES, '168453549861030', '25dd90990d7444d4c8b7a5467ac6bc43')
	
	if facebook_user:
		facebook_graph = Facebook.GraphAPI(facebook_user['access_token'])
		facebook_profile = facebook_graph.get_object('me')
		facebook_friends = facebook_graph.get_connections('me', 'friends')
		
		friends = facebook_friends['data']
		
	elif debug:
		friends = debug_facebook_friends_data
	
	return friends
	
def get_quality_of_life(request, user=None):
	
	# init
	identity = request.user
	records = False
	total_quality = 0
	num_records_with_value = 0
	average = 0
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get all user records
	records = apps.records.models.Record.objects.all().filter(user=user)
	
	# go through all the records and add up the total record quality
	for record in records:
		if record.quality >= 0:
			total_quality = total_quality + record.quality
			num_records_with_value += 1
	
	# get the average (aka: quality)
	if num_records_with_value > 0:
		average = total_quality / num_records_with_value
	
	return average
	
def update_quality_of_life(user=None):
	
	# init
	user_registration_profile = apps.accounts.models.RegistrationProfile.objects.get(user=user)
	user_registration_profile.save() # by calling save, we update quality_of_life
	
	return user_registration_profile.quality_of_life
	
def update_last_viewed_friends_shared(user=None):
	
	# init
	user_registration_profile = apps.accounts.models.RegistrationProfile.objects.get(user=user)
	
	user_registration_profile.last_viewed_friends_shared = datetime.now()
	user_registration_profile.save()
	
	return user_registration_profile