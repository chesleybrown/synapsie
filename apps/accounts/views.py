import sys, pprint
import apps.session_messages as SessionMessages

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404

from apps.accounts.messages import AccountMessages
from apps.accounts.forms import UserCreationForm
from apps.records.models import Record
from apps.tags.utils import get_used_tags, get_popular_tags
from tagging.models import Tag, TaggedItem

def register(request):
	
	# init
	messages = AccountMessages()
	register_formset = UserCreationForm(prefix='register')
	
	if request.method == 'POST':
		register_formset = UserCreationForm(request.POST, prefix='register')
		
		# validate form
		if register_formset.is_valid():
			new_user = register_formset.save()
			
			# message
			SessionMessages.create_message(request, messages.get('created', {
				'account_username': new_user.username,
			}))
			
			return HttpResponseRedirect("/accounts/created/")
	
	return render_to_response("about/home.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))


def created(request):
	
	return render_to_response("accounts/created.html", {
	}, context_instance=RequestContext(request))

def login(request):
	
	# init
	messages = AccountMessages()
	user = None
	user_by_email = None
	
	if request.method == 'POST':
		email = request.POST['username']
		username = request.POST['username']
		password = request.POST['password']
		
		# try to authenticate user (assuming username provided)
		user = auth.authenticate(username=username, password=password)
		
		# if authenticate didn't pass, can also take email and login with that
		if user is None:
			try:
				user_by_email = User.objects.get(email__exact=email)
				
				if user_by_email:
					user = auth.authenticate(username=user_by_email.username, password=password)
				
			# now user found with that email address
			except User.DoesNotExist:
				user_by_email = False
		
		if user and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			
			# Redirect to a success page.
			return HttpResponseRedirect("/records/")
		else:
			# Show an error page
			SessionMessages.create_message(request, messages.get('invalid'))
	
	return HttpResponseRedirect("/")

def logout(request):
	
	# init
	messages = AccountMessages()
	
	auth.logout(request)
	
	# message
	SessionMessages.create_message(request, messages.get('logged_out'))
	
	# Redirect to a success page.
	return HttpResponseRedirect("/")

def profile(request, user_id=0, username=False):
	
	# init
	identity = request.user
	user = identity
	record_stats = {
		'total': 0,
		'personal': 0,
		'shared': 0,
	}
	tag_stats = {
		'total': 0,
		'unique': 0,
		'average_per_record': 0,
	}
	popular_tags_printable = list()
	
	''' Disabling ability to view another user's profile
	# if they provided an id, get that user instead
	if (user_id):
		try:
			# get user
			user = User.objects.get(pk=user_id)
			
		except User.DoesNotExist:
			raise Http404
	
	# if they provided a username
	elif (username):
		try:
			# get user
			user = User.objects.get(username=username)
			
		except User.DoesNotExist:
			raise Http404
	
	# test permission to view
	'''
	
	# get all user records
	records = Record.objects.all().filter(user=user)
	
	# get record stats
	record_stats['total'] = Record.objects.all().filter(user=user).count()
	record_stats['personal'] = records.filter(personal=True).count()
	record_stats['shared'] = records.filter(personal=False).count()
	
	# get tag stats
	unique_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity), counts=True)
	tag_stats['unique'] = len(unique_tags)
	
	for tag in unique_tags:
		tag_stats['total'] += tag.count
	
	if tag_stats['total']:
		tag_stats['average_per_record'] = float(tag_stats['total']) / float(record_stats['total'])
		tag_stats['average_per_record'] = round(tag_stats['average_per_record'], 1)
	
	# get used/popular tags for current user
	used_tags = get_used_tags(Record, identity)
	popular_tags = get_popular_tags(used_tags)
	
	# render
	return render_to_response('accounts/profile.html', {
		'viewed_user': user,
		'record_stats': record_stats,
		'tag_stats': tag_stats,
		'used_tags': used_tags,
		'popular_tags': popular_tags,
	}, context_instance=RequestContext(request))