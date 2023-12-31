import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.accounts import services as AccountService
from apps.tags.messages import TagMessages
from apps.records.models import Record
from apps.tags.forms import TagForm
from tagging.models import Tag, TaggedItem
from tagging.managers import ModelTaggedItemManager

class AnonymousTagHandler(AnonymousBaseHandler):
	model = Tag
	allowed_methods = ('GET')
	fields = ('id', 'text')

class TagHandler(BaseHandler):
	anonymous = AnonymousTagHandler
	allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
	model = Tag
	
	def read(self, request, tag_name=None, page=1):
		
		#init
		identity = request.user
		clean = None
		messages = TagMessages()
		response = dict(
			message = {},
			data = {},
		)
		results_per_page = 10
		clean_tag = None
		clean_tags = list()
		
		# get all user tags
		tag_list = Tag.objects.usage_for_model(Record, filters=dict(user=identity), counts=True)
		
		# sort by count
		tag_list.sort(key=lambda x: x.count, reverse=True)
		
		count = 0
		# clean for return
		for tag in tag_list:
			
			count = count + 1
			clean_tag = {
				'name': tag.name,
				'count': tag.count,
			}
			clean_tags.append(clean_tag)
			
			if count >= results_per_page:
				break
		
		# order by count
		clean_tags_sorted = sorted(clean_tags, key=lambda k: k['count'], reverse=True)
		
		# return message and record updated
		response['message'] = messages.get('found')
		response['data'] = clean_tags_sorted
		
		return response
	
	#@validate(TagForm)
	def create(self, request):
		
		#init
		identity = request.user
		
	
	def update(self, request, tag_name):
		
		# init
		identity = request.user
		tagged_item_manager = ModelTaggedItemManager()
		tag = Tag()
		updated_tag = Tag()
		str_tags = ','
		clean = None
		clean_records = list()
		clean_tag = list()
		messages = TagMessages()
		response = dict(
			message = {},
			data = {},
		)
		formset = None
		
		# get original tag
		try:
			tag = Tag.objects.get(name=tag_name)
			
		except Tag.DoesNotExist:
			response['message'] = messages.get('not_found')
			return response
		
		# not allowed to update a facebook_id's name
		if tag.facebook_id:
			response['message'] = messages.get('permission_denied')
			return response
		
		# get updated tag (if it exists already)
		try:
			updated_tag = Tag.objects.get(name=request.PUT['name'].lower())
			
		except Tag.DoesNotExist:
			updated_tag = None
		
		# UPDATED TAG formset
		if updated_tag:
			formset = TagForm(request.PUT, instance=updated_tag)
		
		# tag doesn't exist yet... new tag
		else:
			formset = TagForm(request.PUT)
		
		# validate form
		if formset.is_valid():
			clean = formset.cleaned_data
			
			# create "updated" tag as a new tag if it doesn't exist already
			if not updated_tag:
				updated_tag = Tag(
					name = clean['name']
				)
			
			# get all records with the original tag
			records = Record.objects.all().filter(user=identity)
			tagged_records = tagged_item_manager.with_all("," + tag.name, records)
			
			# go through each record and update the tags for them
			for tagged_record in tagged_records:
				
				# basically go through all the record's current tags and remove
				# the one the user is currently updating
				record_tags = list()
				record_tags_list = list()
				for record_tag in tagged_record.tags:
					if record_tag.name != tag_name:
						record_tags.append(record_tag)
						record_tags_list.append(record_tag.name)
				
				record_tags.append(updated_tag)
				record_tags_list.append(updated_tag.name)
				
				# set all the info for the updated record
				clean_record = {
					'id': tagged_record.id,
					'user_id': tagged_record.user_id,
					'text': tagged_record.text,
					'personal': tagged_record.personal,
					'created': tagged_record.created,
					'happened': tagged_record.happened,
					'tags': record_tags,
				}
				clean_records.append(clean_record)
				
				# update the tags for the records
				str_tags = "," + ",".join(record_tags_list)
				Tag.objects.update_tags(tagged_record, str_tags)
				
				# update the quality for each record
				tagged_record.save(update_quality_of_life=False)
			
			# now update user's quality of life
			AccountService.update_quality_of_life(identity)
			
			# return clean updated tag
			clean_tag = {
				'name': updated_tag.name,
			}
			
			# return message and record updated
			response['message'] = messages.get('updated', {
				'tag_name': tag_name,
			})
			response['data'] = clean_tag
			
		else:
			response['message'] = messages.get('invalid')
		
		return response
	
	def delete(self, request, tag_name, record_id=None):
		
		# init
		identity = request.user
		tag = None
		records = None
		tagged_item_manager = ModelTaggedItemManager()
		tagged_item_ids = []
		record_type = ContentType.objects.get_for_model(Record)
		messages = TagMessages()
		response = dict(
			message = {},
			data = {},
		)
		clean_tag = list()
		
		# get id of tag
		try:
			tag = Tag.objects.get(name=tag_name)
			
		except Tag.DoesNotExist:
			raise Http404
		
		# get tagged records (if no record_id provided)
		if (record_id):
			try:
				tagged_record = Record.objects.get(pk=record_id, user=identity)
				
			except Record.DoesNotExist:
				raise Http404
			
			tagged_items = TaggedItem.objects.all().filter(object_id=tagged_record.id, tag=tag, content_type=record_type)
			
			# delete it
			tagged_items.delete()
			
			# update record quality of life
			tagged_record.save()
			
		# doing a global tag delete for user
		else:
			records = Record.objects.all().filter(user=identity)
			tagged_records = tagged_item_manager.with_all(tag_name, records)
			
			for tagged_record in tagged_records:
				tagged_item_ids.append(tagged_record.id)
				
				# update the quality for each record
				tagged_record.save(update_quality_of_life=False)
			
			tagged_items = TaggedItem.objects.all().filter(object_id__in=tagged_item_ids, tag=tag, content_type=record_type)
			
			# delete them
			tagged_items.delete()
			
			# update user's quality of life
			AccountService.update_quality_of_life(identity)
		
		# return clean deleted tag
		clean_tag = {
			'name': tag.name,
		}
		
		# return delete message
		response['message'] = messages.get('deleted', {
			'tag_name': tag_name,
		})
		response['data'] = clean_tag
		return response