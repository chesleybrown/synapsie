import sys
import apps.session_messages as SessionMessages

from apps.tags.messages import TagMessages
from apps.records.models import Record
from apps.tags.forms import TagForm
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list


@login_required
def index_tags(request, page=1):
	
	# init
	identity = request.user
	tag_list = False
	tags = False
	tags_paginator = False
	selected_tags = False
	popular_tags_printable = list()
	results_per_page = 500
	paginator = False
	
	# get all user tags
	tag_list = Tag.objects.usage_for_model(Record, filters=dict(user=identity), counts=True)
	
	# number of items per page
	paginator = Paginator(tag_list, results_per_page)
	
	# If page request is out of range, deliver last page of results.
	try:
		tags_paginator = paginator.page(page)
	except (EmptyPage, InvalidPage):
		tags_paginator = paginator.page(paginator.num_pages)
	
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
	return render_to_response('tags/tag_index.html', {
		'selected_tags': selected_tags,
		'used_tags_printable': used_tags_printable,
		'used_tags': used_tags,
		'popular_tags': popular_tags_printable,
		'tags_paginator': tags_paginator,
		'tags_per_page': results_per_page,
	}, context_instance=RequestContext(request))

@login_required
def list_tags(request):
	
	# init
	identity = request.user
	records = False
	
	# get tags user has used
	tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity))
	
	# render
	return render_to_response('tags/tag_list.html', {
		'tags': tags,
	}, context_instance=RequestContext(request))

@login_required
def add_tag(request):
	
	# init
	identity = request.user
	formset = TagForm()
	
	# test permission to edit
	#if not record.can_edit(identity):
	#	return HttpResponseRedirect(reverse('record_list'))
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity))
	used_tags_printable = ", ".join(map(str, used_tags))
	
	# if user has posted
	if request.method == 'POST':
		
		formset = TagForm(request.POST)
		
		# validate form
		if formset.is_valid():
			clean = formset.cleaned_data
			
			# add record
			#tag.name = clean['name']
			
			# save
			#tag.save()
			
			# update tags
			#Tag.objects.update_tags(record, clean['tags'])
			
			# redirect to show_record
			#return HttpResponseRedirect(reverse('tag_show', kwargs=dict(tag_id=tag.id)))
	
	# render
	return render_to_response('tags/tag_form.html', {
		'formset': formset,
		'used_tags_printable': used_tags_printable,
	}, context_instance=RequestContext(request))

@login_required
def show_tag(request, tag_id):
	
	# init
	identity = request.user
	
	# get record
	tag = Tag.objects.get(pk=tag_id)
	
	# check if record was found
	if tag is None:
		raise Http404
	
	# test permission to view
	#if not record.can_view(identity):
	#	return HttpResponseRedirect(reverse('record_list'))
	
	# find all associated tags
	#record_tags = Tag.objects.get_for_object(record)
	
	# render
	return render_to_response('tags/tag_detail.html', {
		'tag': tag,
	}, context_instance=RequestContext(request))

@login_required
def edit_tag(request, tag_id):
	
	# init
	identity = request.user
	formset = TagForm()
	
	# get record
	tag = Tag.objects.get(pk=tag_id)
	
	# check if record was found
	if tag is None:
		raise Http404
	
	# test permission to edit
	#if not record.can_edit(identity):
	#	return HttpResponseRedirect(reverse('record_list'))
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(Record, filters=dict(user=identity))
	used_tags_printable = ", ".join(map(str, used_tags))
	
	#record.tags = tags
	formset = TagAdminForm(instance=tag)
	
	# if user has posted
	if request.method == 'POST':
		
		formset = TagForm(request.POST)
		
		# validate form
		if formset.is_valid():
			clean = formset.cleaned_data
			
			# update record
			tag.name = clean['name']
			
			# save
			tag.save()
			
			# redirect to show_record
			return HttpResponseRedirect(reverse('tag_show', kwargs=dict(tag_id=tag.id)))
	
	# render
	return render_to_response('tags/tag_form.html', {
		'object' : tag,
		'formset': formset,
		'used_tags_printable': used_tags_printable,
	}, context_instance=RequestContext(request))

@login_required
def delete_tag(request, tag_id):
	
	# init
	identity = request.user
	
	# get record
	tag = Tag.objects.get(pk=tag_id)
	
	# check if record was found
	if tag is None:
		raise Http404
	
	user_records = Record.objects.all().filter(user=identity)
	tagged_user_records = TaggedItem.objects.get_by_model(user_records, tag)
	
	#for tagged_user_record in tagged_user_records:
	#	sys.exit(TaggedItem.objects.all().filter(content_type=tagged_user_record, object_id=tagged_user_record.id, tag=tag_id))
	#	tagged_item = TaggedItem.objects.all().filter(content_type=tagged_user_record, object_id=tagged_user_record.id, tag=tag_id)
	#	tagged_item.delete()
	
	# test permission to delete
	#if not tag.can_delete(identity):
	#	return HttpResponseRedirect(reverse('record_list'))
	
	# delete it
	#tag.delete()
	
	# redirect to show_record
	return HttpResponseRedirect(reverse('tag_list'))