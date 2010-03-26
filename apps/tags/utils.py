from tagging.models import Tag, TaggedItem

def get_used_tags(model, user):
	
	# get available tags user has used
	used_tags = Tag.objects.usage_for_model(model, filters=dict(user=user), counts=True)
	#used_tags_printable = ", ".join(map(str, used_tags))
	
	return used_tags
	

def get_popular_tags(used_tags):
	
	# init
	highest = False
	popular_tags_list = list()
	
	popular_tags = sorted(used_tags, key=lambda x: x.count, reverse=True)
	
	# get popular tags ready for template
	if (popular_tags):
		highest = popular_tags[0]
		for tag in popular_tags:
			tag.percent = round((float(tag.count) / float(highest.count)) * 100, 0)
			popular_tags_list.append(tag)
	
	return popular_tags_list
	