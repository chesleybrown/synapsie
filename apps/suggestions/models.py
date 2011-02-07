from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag

class Suggestion(models.Model):
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	priority = models.IntegerField(max_length=3, null=True)
	
	def __unicode__(self):
		return 'Suggestion: %s' % self.text
	
	def delete(self):
		
		# before deleting, remove associated tags
		tagged_items = Tag.objects.update_tags(self, None)
		
		super(Suggestion, self).delete()
	
	# tags property
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	
	tags = property(get_tags)
	
	# clean tags property
	def get_clean_tags(self):
		clean_tags = []
		tags = Tag.objects.get_for_object(self)
		
		for tag in tags:
			clean_tags.append({
				'id': tag.id,
				'name': tag.name,
			})
		
		return clean_tags
	
	clean_tags = property(get_clean_tags)
	
	def get_tags_printable(self):
		suggestion_tags = self.get_tags()
		tags_printable = ", ".join(map(str, suggestion_tags))
		return tags_printable
	
class UserSuggestions(models.Model):
	user = models.ForeignKey(User)
	suggestion = models.ForeignKey(Suggestion)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	ignored = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)
	viewed = models.BooleanField(default=False)
	
	def __unicode__(self):
		return 'User Suggestion: %s' % self.id