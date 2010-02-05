import datetime

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.records.models import Record
from apps.records.forms import RecordForm
from tagging.models import Tag

class AnonymousRecordHandler(AnonymousBaseHandler):
	model = Record
	allowed_methods = ('GET')
	fields = ('id', 'text')

class RecordHandler(BaseHandler):
	anonymous = AnonymousRecordHandler
	allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
	model = Record
	
	def read(self, request, record_id=None):
		
		#init
		identity = request.user
		
		if record_id is not None:
			record = Record.objects.get(pk=record_id)
			
			# check if record was found
			if record is None:
				return False
			
			# test permission to view
			if not record.can_view(identity):
				return False
			
			return record
		
		paginator = Paginator(Record.objects.all(), 25)
		return paginator.page(int(request.GET.get('page', 1))).object_list
	
	@validate(RecordForm)
	def create(self, request):
		
		#init
		identity = request.user
		formset = RecordForm()
		now = datetime.datetime.now()
		str_tags = ''
		
		# if user has posted
		if request.method == 'POST':
			
			formset = RecordForm(request.POST)
			arr_tags = request.POST.getlist('tags[]')
			
			# validate form
			if formset.is_valid():
				clean = formset.cleaned_data
				
				# create record, set user
				record = Record(
					user_id = identity.id,
					text = clean['text'],
					personal = int(clean['personal'])
				)
				
				# save
				record.save()
				
				# add tags
				str_tags = ",".join(arr_tags)
				Tag.objects.update_tags(record, str_tags)
				
				# return only what we need to
				clean_record = {
					'id': record.id,
					'user_id': record.user_id,
					'text': record.text,
					'personal': record.personal,
					'created': record.created,
					'tags': record.tags
				}
				
				# redirect to show_record
				return clean_record
		
		return record
	
	def update(self, request, record_id):
		return rc.UPDATED
	
	def delete(self, request, record_id):
		
		# init
		identity = request.user
		
		# get record
		record = Record.objects.get(pk=record_id)
		
		# check if record was found
		if record is None:
			raise Http404
		
		# test permission to delete
		if not record.can_delete(identity):
			SessionMessages.create_message(request, messages.get('permission_denied'))
			return HttpResponseRedirect(reverse('record_index'))
		
		# delete it
		record.delete()
		
		return rc.DELETED