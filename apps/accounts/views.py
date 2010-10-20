import datetime
import sys, pprint
import apps.session_messages as SessionMessages
import logging

from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404
from django.core.mail import EmailMultiAlternatives

from apps.accounts.models import RegistrationManager, RegistrationProfile
from apps.accounts.messages import AccountMessages
from apps.accounts.emails import AccountEmails
from apps.accounts.forms import UserCreationForm, UserPasswordResetForm, UserPasswordResetConfirmationForm
from apps.records.models import Record
from apps.tags.utils import get_used_tags, get_popular_tags
from tagging.models import Tag, TaggedItem

# Get an instance of a logger
logger = logging.getLogger('django')

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
			email = EmailMultiAlternatives(user_email['subject'], user_email['body'], user_email['from_address'], [new_user.email])
			email.attach_alternative(user_email['body'], "text/html")
			email.send()
			
			# also send it to me
			email = EmailMultiAlternatives(user_email['subject'], user_email['body'], user_email['from_address'], ['chesley@synapsie.com'])
			email.attach_alternative(user_email['body'], "text/html")
			email.send()
			
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

def reset(request):
	
	# init
	emails = AccountEmails()
	messages = AccountMessages()
	user = None
	user_registration_profile = None
	account_reset_formset = UserPasswordResetForm(prefix='account_reset')
	
	# if form was submitted
	if request.method == 'POST':
		account_reset_formset = UserPasswordResetForm(request.POST, prefix='account_reset')
		
		# validate form
		if account_reset_formset.is_valid():
			clean = account_reset_formset.cleaned_data
			
			# test if there is a user that matches the provided email
			try:
				user = User.objects.get(email__exact=clean['email'])
				
			# no user found with that email address
			except User.DoesNotExist:
				user = None
			
			# get user registration profile
			try:
				user_registration_profile = RegistrationProfile.objects.get(user=user)
				
			# no user found with that email address
			except RegistrationProfile.DoesNotExist:
				user_registration_profile = None
			
			# user was found and is marked "active"
			if user and user_registration_profile and user.is_active:
				
				# Generate reset_key
				user_registration_profile.generate_reset_key(user)
				
				# generate email and send it to user
				user_email = emails.get('reset', {
					'account_first_name': user.first_name,
					'account_last_name': user.last_name,
					'account_reset_key': user_registration_profile.reset_key,
				})
				email = EmailMultiAlternatives(user_email['subject'], user_email['body'], user_email['from_address'], [user.email])
				email.attach_alternative(user_email['body'], "text/html")
				email.send()
				
				# inform user they have been emailed
				SessionMessages.create_message(request, messages.get('password_reset', {
					'account_email': clean['email'],
				}))
				
				# Redirect to a homepage.
				return HttpResponseRedirect("/")
				
			else:
				# Show an error page
				SessionMessages.create_message(request, messages.get('email_not_found', {
					'account_email': clean['email'],
				}))
		
	return render_to_response("accounts/reset.html", {
		'account_reset_formset': account_reset_formset,
	}, context_instance=RequestContext(request))

def resetconfirmation(request, reset_key):
	
	# init
	emails = AccountEmails()
	messages = AccountMessages()
	user = None
	user_registration_profile = None
	accounts_resetconfirmation_formset = UserPasswordResetConfirmationForm(
		initial={'reset_key': reset_key},
		prefix='account_resetconfirmation'
	)
	
	# if form was submitted
	if request.method == 'POST':
		accounts_resetconfirmation_formset = UserPasswordResetConfirmationForm(request.POST, prefix='account_resetconfirmation')
		
		# validate form
		if accounts_resetconfirmation_formset.is_valid():
			clean = accounts_resetconfirmation_formset.cleaned_data
			
			# update user password if correct reset_key provided (also disables the key after password is updated)
			accounts_resetconfirmation_formset.save()
			
			SessionMessages.create_message(request, messages.get('password_updated'))
			
			# Redirect to a homepage.
			return HttpResponseRedirect("/")
			
	else:
		# test if valid reset_key provided
		try:
			user_registration_profile = RegistrationProfile.objects.get(reset_key=reset_key)
			
		except RegistrationProfile.DoesNotExist:
			SessionMessages.create_message(request, messages.get('invalid_reset_key'))
			return HttpResponseRedirect("/")
	
	return render_to_response("accounts/resetconfirmation.html", {
		'accounts_resetconfirmation_formset': accounts_resetconfirmation_formset,
		'reset_key': reset_key,
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
				
			# no user found with that email address
			except User.DoesNotExist:
				user_by_email = None
		
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