from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from apps.accounts import services as AccountService

class Record(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	happened = models.DateTimeField()
	personal = models.SmallIntegerField(default=1)
	quality = models.FloatField(null=True, max_length=6)
	
	def __unicode__(self):
		return 'Record: %s' % self.text
	
	def delete(self):
		
		# before deleting, remove associated tags
		tagged_items = Tag.objects.update_tags(self, None)
		
		super(Record, self).delete()
	
	# tags property
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	
	tags = property(get_tags)
	
	# record_quality property (calculates qualty of record)
	def get_quality(self):
		
		# init
		total = 0
		average = 0
		num_tags_with_value = 0
		
		# loop through all record tags and get the total of the tag values
		for tag in self.tags:
			if tag.value >= 0:
				total = total + tag.value
				num_tags_with_value += 1
		
		# get the average (aka: quality)
		if num_tags_with_value > 0:
			average = total / num_tags_with_value
		
		else:
			average = None
		
		return average
	
	#quality = property(get_quality)
	
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
		record_tags = self.get_tags()
		tags_printable = ", ".join(map(str, record_tags))
		return tags_printable
	
	# test to see if given user owns this record
	def is_owner(self, user):
		
		# must provide valid user
		if not isinstance(user, User):
			return False
		
		# if user is not owner of item
		if not self.user.id == user.id:
			return False
		
		# user is owner
		return True
	
	# test to see if given user can view this record
	def can_view(self, user):
		
		# anyone can view if it isn't private
		if not self.personal:
			return True
		
		# if it is private, than only owner can view
		return self.is_owner(user)
	
	# test to see if given user can edit this record
	def can_edit(self, user):
		return self.is_owner(user)
	
	# test to see if given user can delete this record
	def can_delete(self, user):
		return self.is_owner(user)
	
	# this hook is for setting the record quality
	def save(self):
		
		# init
		self.quality = self.get_quality()
		
		# Call the "real" save() method
		super(Record, self).save()
		
		# also update user's quality of life
		AccountService.update_quality_of_life(self.user)