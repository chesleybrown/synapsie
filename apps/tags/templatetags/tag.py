from django import template

register = template.Library()

@register.inclusion_tag('tags/templatetags/tag.html')
def render_tag(tag, close_url=False, closebutton_class=''):
	return {
		'tag': tag,
		'close_url': close_url,
		'closebutton_class': closebutton_class,
	}

@register.inclusion_tag('tags/templatetags/tags.html')
def render_tags(tags, close_url=False, closebutton_class=''):
	return {
		'tags': tags,
		'close_url': close_url,
		'closebutton_class': closebutton_class,
	}