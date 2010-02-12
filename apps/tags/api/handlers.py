import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.records.models import Record
#from apps.tags.forms import TagForm
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
	
	def read(self, request, tag_name=None):
		
		#init
		identity = request.user
	
	#@validate(TagForm)
	def create(self, request):
		
		#init
		identity = request.user
		
	
	def update(self, request, tag_id):
		return rc.UPDATED
	
	def delete(self, request, tag_name, record_id=None):
		
		# init
		identity = request.user
		tag = None
		records = None
		tagged_item_manager = ModelTaggedItemManager()
		tagged_item_ids = []
		record_type = ContentType.objects.get_for_model(Record)
		
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
			
		# doing a global tag delete for user
		else:
			records = Record.objects.all().filter(user=identity)
			tagged_records = tagged_item_manager.with_all(tag_name, records)
			
			for tagged_record in tagged_records:
				tagged_item_ids.append(tagged_record.id)
			
			tagged_items = TaggedItem.objects.all().filter(object_id__in=tagged_item_ids, tag=tag, content_type=record_type)
			
		# delete it/them
		tagged_items.delete()
		
		return rc.DELETED