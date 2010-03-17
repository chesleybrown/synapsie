from django import template

from tagging.models import Tag

register = template.Library()

@register.inclusion_tag('tags/templatetags/tag.html')
def render_tag(tag=None, close_url=False, closebutton_class=''):

	# if no tag provided... generate an empty tag
	if (tag is None):
		tag = Tag()
	
	return {
		'tag': tag,
		'close_url': close_url,
		'closebutton_class': closebutton_class,
	}

@register.inclusion_tag('tags/templatetags/tags.html')
def render_tags(tags=None, close_url=False, closebutton_class=''):
	
	# if no tag provided... generate an empty tag
	if (tags is None):
		tag = Tag()
		tags = [tag]
	
	return {
		'tags': tags,
		'close_url': close_url,
		'closebutton_class': closebutton_class,
	}