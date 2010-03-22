from django.db import models
from django import forms

from tagging.models import Tag
from tagging.forms import TagField

class TagForm(forms.ModelForm):
	name = forms.RegexField(r'^[^,]*$')
	
	class Meta:
		model = Tag
