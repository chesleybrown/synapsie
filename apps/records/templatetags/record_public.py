from django import template

from apps.records.models import Record

register = template.Library()

@register.inclusion_tag('records/templatetags/record_public.html')
def render_record_public(record=None):
	
	# if no tag provided... generate an empty tag
	if (record is None):
		record = Record()
	
	return {
		'record': record,
	}