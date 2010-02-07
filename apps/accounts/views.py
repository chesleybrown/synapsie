import apps.session_messages as SessionMessages

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404

from apps.accounts.messages import AccountMessages
from apps.accounts.forms import UserCreationForm

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

def show(request, user_id=0, username=False):
	
	# init
	identity = request.user
	user = identity
	
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
	
	# render
	return render_to_response('accounts/show.html', {
		'user': user,
	}, context_instance=RequestContext(request))