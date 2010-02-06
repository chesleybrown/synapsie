import sys, pprint
import apps.session_messages as SessionMessages

from apps.records.messages import RecordMessages
from apps.records.models import Record
from apps.records.forms import RecordForm
from tagging.models import Tag, TaggedItem
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

@login_required
def index_records(request, tags=False):
	
	# init
	identity = request.user
	records = False
	formset = RecordForm()
	selected_tags = False
	popular_tags_printable = list()
	
	# get user records
	records = Record.objects.all().filter(user=identity).order_by('-created')
	
	# filter by tags if provided
	if (tags):
		selected_tags = tags.split(",")
		records = TaggedItem.objects.get_by_model(records, selected_tags)
		
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity), counts=True)
	used_tags_printable = ", ".join(map(str, used_tags))
	popular_tags = sorted(used_tags, key=lambda x: x.count, reverse=True)
	
	# get popular tags ready for template
	highest = popular_tags[0]
	for tag in popular_tags:
		tag.percent = (float(tag.count) / float(highest.count)) * 100
		popular_tags_printable.append(tag)
	
	# render
	return render_to_response('records/record_index.html', {
		'formset': formset,
		'selected_tags': selected_tags,
		'used_tags_printable': used_tags_printable,
		'used_tags': used_tags,
		'popular_tags': popular_tags_printable,
		'object_list': records,
	}, context_instance=RequestContext(request))
	
	return object_list(request, records, paginate_by=10)

def public_records(request, user_id=0, username=False):
	
	# init
	identity = request.user
	user = identity
	records = False
	
	try:
		# if a user is provided, get that user's public records instead
		if user_id:
			user = User.objects.get(pk=user_id)
		
		# if a username is provided, get by that instead
		elif username:
			user = User.objects.get(username__iexact=username)
		
	except User.DoesNotExist:
		raise Http404
	
	# get user records
	records = Record.objects.all().filter(user=user, personal=0).order_by('-created')
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=user), counts=True)
	used_tags_printable = ", ".join(map(str, used_tags))
	popular_tags = sorted(used_tags, key=lambda x: x.count, reverse=True)[:5]
	
	# render
	return render_to_response('records/record_public.html', {
		'used_tags': used_tags,
		'popular_tags': popular_tags,
		'object_list': records,
	}, context_instance=RequestContext(request))
	
	return object_list(request, records, paginate_by=10)

@login_required
def list_records(request):
	
	# init
	identity = request.user
	records = False
	
	# get user records
	records = Record.objects.all().filter(user=identity).order_by('-created')
	
	return object_list(request, records, paginate_by=10)

@login_required
def add_record(request):
	
	# init
	identity = request.user
	messages = RecordMessages()
	formset = RecordForm()
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity))
	used_tags_printable = ", ".join(map(str, used_tags))
	
	# if user has posted
	if request.method == 'POST':
		
		formset = RecordForm(request.POST)
		
		# validate form
		if formset.is_valid():
			clean = formset.cleaned_data
			
			# create record, set user
			record = Record(
				user = identity,
				text = clean['text'],
				personal = int(clean['personal'])
			)
			
			# save
			record.save()
			
			# add tags
			Tag.objects.update_tags(record, clean['tags'])
			
			# message
			SessionMessages.create_message(request, messages.get('created', {
				'record_text': record.text,
			}))
			
			# redirect to show_record
			#return HttpResponseRedirect(reverse('record_show', kwargs=dict(record_id=record.id)))
			return HttpResponseRedirect(reverse('record_index'))
	
	# render
	return render_to_response('records/record_form.html', {
		'formset': formset,
		'used_tags_printable': used_tags_printable,
	}, context_instance=RequestContext(request))

@login_required
def show_record(request, record_id):
	
	# init
	identity = request.user
	
	try:
		# get record
		record = Record.objects.get(pk=record_id)
		
	except Record.DoesNotExist:
		raise Http404
	
	# test permission to view
	if not record.can_view(identity):
		return HttpResponseRedirect(reverse('record_list'))
	
	# find all associated tags
	#record_tags = Tag.objects.get_for_object(record)
	
	# render
	return render_to_response('records/record_detail.html', {
		'record': record,
	}, context_instance=RequestContext(request))

@login_required
def edit_record(request, record_id):
	
	# init
	identity = request.user
	formset = RecordForm()
	
	# get record
	record = Record.objects.get(pk=record_id)
	
	# check if record was found
	if record is None:
		raise Http404
	
	# test permission to edit
	#if not record.can_edit(identity):
	#	return HttpResponseRedirect(reverse('record_list'))
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity))
	used_tags_printable = ", ".join(map(str, used_tags))
	
	# populate form
	formset = RecordForm(instance=record)
	
	# if user has posted
	if request.method == 'POST':
		
		formset = RecordForm(request.POST)
		
		# validate form
		if formset.is_valid():
			clean = formset.cleaned_data
			
			# update record
			record.text = clean['text']
			record.personal = int(clean['personal'])
			
			# save
			record.save()
			
			# update tags
			Tag.objects.update_tags(record, clean['tags'])
			
			# redirect to show_record
			return HttpResponseRedirect(reverse('record_show', kwargs=dict(record_id=record.id)))
	
	# render
	return render_to_response('records/record_form.html', {
		'object' : record,
		'formset': formset,
		'used_tags_printable': used_tags_printable,
	}, context_instance=RequestContext(request))

@login_required
def delete_record(request, record_id):
	
	# init
	identity = request.user
	messages = RecordMessages()
	
	# get record
	record = Record.objects.get(pk=record_id)
	
	# check if record was found
	if record is None:
		raise Http404
	
	# test permission to delete
	if not record.can_delete(identity):
		SessionMessages.create_message(request, messages.get('permission_denied'))
		return HttpResponseRedirect(reverse('record_index'))
	
	# message
	SessionMessages.create_message(request, messages.get('deleted', {
		'record_text': record.text,
	}))
	
	# delete it
	record.delete()
	
	# redirect to list_records
	return HttpResponseRedirect(reverse('record_index'))