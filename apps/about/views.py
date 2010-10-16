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

def home(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	# if user is logged in, redirect to records
	if not identity.is_anonymous():
		return HttpResponseRedirect("/records/")
	
	return render_to_response("about/home.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
	
def about(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	return render_to_response("about/about.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
	
def terms(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	return render_to_response("about/terms.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
	
def privacy(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	return render_to_response("about/privacy.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
	
def acceptableuse(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	return render_to_response("about/acceptableuse.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))
	
def copyright(request):
	
	# init
	identity = request.user
	register_formset = UserCreationForm(prefix='register')
	
	return render_to_response("about/copyright.html", {
		'register_formset': register_formset,
	}, context_instance=RequestContext(request))