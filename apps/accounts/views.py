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
from tagging.models import Tag, TaggedItem

def register(request):
	
	# init
	messages = AccountMessages()
	formset = UserCreationForm()
	
	if request.method == 'POST':
		formset = UserCreationForm(request.POST)
		
		# validate form
		if formset.is_valid():
			new_user = formset.save()
			
			# message
			SessionMessages.create_message(request, messages.get('created', {
				'account_username': new_user.username,
			}))
			
			return HttpResponseRedirect("/accounts/created/")
	
	return render_to_response("accounts/register.html", {
		'formset': formset,
	}, context_instance=RequestContext(request))


def login(request):
	
	# init
	messages = AccountMessages()
	user = None
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
	
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			
			# message
			SessionMessages.create_message(request, messages.get('logged_in', {
				'account_username': user.username,
			}))
			
			# Redirect to a success page.
			return HttpResponseRedirect("/records/")
		else:
			# Show an error page
			return HttpResponseRedirect("/account/invalid/")
	
	return render_to_response('accounts/login.html', {
	}, context_instance=RequestContext(request))

def logout(request):
	
	# init
	messages = AccountMessages()
	
	auth.logout(request)
	
	# message
	SessionMessages.create_message(request, messages.get('logged_out'))
	
	# Redirect to a success page.
	return HttpResponseRedirect("/accounts/login/")

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
	
	tag_stats['average_per_record'] = float(tag_stats['total']) / float(record_stats['total'])
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity), counts=True)
	used_tags_printable = ", ".join(map(str, used_tags))
	popular_tags = sorted(used_tags, key=lambda x: x.count, reverse=True)
	
	# get popular tags ready for template
	if (popular_tags):
		highest = popular_tags[0]
		for tag in popular_tags:
			tag.percent = (float(tag.count) / float(highest.count)) * 100
			popular_tags_printable.append(tag)
	
	# render
	return render_to_response('accounts/profile.html', {
		'viewed_user': user,
		'record_stats': record_stats,
		'tag_stats': tag_stats,
		'used_tags': used_tags,
		'popular_tags': popular_tags_printable,
	}, context_instance=RequestContext(request))