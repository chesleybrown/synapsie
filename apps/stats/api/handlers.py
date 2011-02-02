from datetime import datetime
import time

from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, validate

from apps.stats.messages import StatMessages

from apps.records.models import Record
from apps.records.forms import RecordForm, RecordAddTagsForm
from apps.records.services import RecordService
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

class AnonymousRecordHandler(AnonymousBaseHandler):
	model = Record
	allowed_methods = ('GET')
	fields = ('id', 'text')

class StatHandler(BaseHandler):
	anonymous = AnonymousRecordHandler
	allowed_methods = ('GET')
	model = Record
	
	# init our empty response
	empty_response = dict(
		message = {},
		data = {},
	)
	
	def read(self, request, type=None):
		
		# init
		identity = request.user
		user = identity
		record_service = RecordService()
		messages = StatMessages()
		message = False
		records = False
		clean_stats = list()
		response = self.empty_response
		
		if type is 'weekly':
			StatService.get_weekly(request, user=user)
		
		return response
	