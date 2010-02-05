from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag

class Record(models.Model):
	user = models.ForeignKey(User)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	personal = models.BooleanField(default=True)
	
	def __unicode__(self):
		return 'Record: %s' % self.text
	
	def delete(self):
		
		# before deleting, remove associated tags
		tagged_items = Tag.objects.update_tags(self, None)
		
		super(Record, self).delete()
	
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	
	tags = property(get_tags)
	
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