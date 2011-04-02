from django.db import models
from django import forms
import settings

from tagging.models import Tag
from tagging.forms import TagField
from django.utils.translation import ugettext_lazy as _

class TagForm(forms.ModelForm):
	name = forms.RegexField(label=_('Name'), regex=r'^[\'\w\-\!\@\#\$\%\^\&\*\(\),\s\.]+$', max_length=settings.MAX_TAG_LENGTH)
	
	def clean_name(self):
		name = str(self.cleaned_data['name'])
		
		# all tags should be lowercase
		if settings.FORCE_LOWERCASE_TAGS:
			name = name.lower()
		
		return name
	
	class Meta:
		model = Tag
		exclude = ('value', 'facebook_name', 'facebook_id')
