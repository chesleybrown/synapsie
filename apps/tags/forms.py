from django import forms
from tagging.models import Tag
from tagging.forms import TagField

class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
