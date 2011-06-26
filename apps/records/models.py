from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from tagging.models import Tag, TaggedItem
from apps.accounts import services as AccountService

class Record(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	happened = models.DateTimeField()
	personal = models.SmallIntegerField(default=1)
	quality = models.FloatField(null=True, max_length=6)
	#tags = generic.GenericRelation(TaggedItem, content_type_field='content_type', object_id_field='object_id')
	tags = list()
	
	def __unicode__(self):
		return 'Record: %s' % self.text
	
	def delete(self):
		
		# before deleting, remove associated tags
		tagged_items = Tag.objects.update_tags(self, None)
		
		super(Record, self).delete()
	
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
				'facebook_name': tag.facebook_name,
				'facebook_id': tag.facebook_id,
			})
		
		return clean_tags
	
	clean_tags = property(get_clean_tags)
	
	def get_tags_printable(self):
		tags_printable = ", ".join(map(str, self.tags))
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
	
	# this hook is for setting the record quality and updating user's quality of life on save
	def save(self, update_quality_of_life=True):
		
		# init
		self.quality = self.get_quality()
		
		# Call the "real" save() method
		super(Record, self).save()
		
		# also update user's quality of life
		if update_quality_of_life:
			AccountService.update_quality_of_life(self.user)
	
	# this hook is for setting the record quality and updating user's quality of life on delete
	def delete(self, update_quality_of_life=True):
		
		# init
		self.quality = self.get_quality()
		
		# Call the "real" delete() method
		super(Record, self).delete()
		
		# also update user's quality of life
		if update_quality_of_life:
			AccountService.update_quality_of_life(self.user)