import sys, pprint
import apps.session_messages as SessionMessages

from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404
from django.core import mail

from apps.accounts.models import RegistrationManager, RegistrationProfile
from apps.accounts.messages import AccountMessages
from apps.accounts.emails import AccountEmails
from apps.accounts.forms import UserCreationForm
from apps.records.models import Record
from apps.tags.utils import get_used_tags, get_popular_tags
from tagging.models import Tag, TaggedItem

def register(request):
	
	# init
	messages = AccountMessages()
	emails = AccountEmails()
	register_formset = UserCreationForm(prefix='register')
	user_email = None
	user_registration_profile = None
	
	if request.method == 'POST':
		register_formset = UserCreationForm(request.POST, prefix='register')
		
		# validate form
		if register_formset.is_valid():
			
			# save the new user to db
			new_user = register_formset.save()
			user_registration_profile = RegistrationProfile.objects.create_profile(new_user)
			
			# generate email and send it to user
			user_email = emails.get('registered', {
				'account_first_name': new_user.first_name,
				'account_last_name': new_user.last_name,
				'account_activation_key': user_registration_profile.activation_key,
			})
			mail.send_mail(user_email['subject'], user_email['body'], user_email['from_address'], [new_user.email], fail_silently=False)
			
			# message
			SessionMessages.create_message(request, messages.get('created', {
				'account_email': new_user.email,
			}))
			
			return HttpResponseRedirect("/accounts/created/")
	
	return render_to_response("about/home.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
register = transaction.commit_on_success(register)

def activate(request, activation_key=None):
	
	# init
	messages = AccountMessages()
	user= None
	
	# activate account if correct key provided
	user = RegistrationProfile.objects.activate_user(activation_key)
	
	# successfully activated
	if user:
		SessionMessages.create_message(request, messages.get('activated', {
			'account_first_name': user.first_name,
			'account_last_name': user.last_name,
		}))
		
		# Correct password, and the user is marked "active"
		user.backend='django.contrib.auth.backends.ModelBackend' # allows me to log user in without knowing password
		auth.login(request, user)
		
		# Redirect to a logged in page.
		return HttpResponseRedirect("/records/")
		
	# failed activating user (incorrect key?)
	else:
		SessionMessages.create_message(request, messages.get('invalid_activation_key'))
	
	# Redirect to a homepage.
	return HttpResponseRedirect("/")

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