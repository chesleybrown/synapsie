from django import forms
from apps.suggestions.models import Suggestion, UserSuggestions
from datetime import date, datetime
from django.utils.translation import ugettext_lazy as _

class UserSuggestionForm(forms.ModelForm):
	completed = forms.BooleanField(
		label=_('Completed'),
		initial=None,
		required=False,
	)
	viewed = forms.BooleanField(
		label=_('Viewed'),
		initial=None,
		required=False,
	)
	
	class Meta:
		model = UserSuggestions
		exclude = ('created', 'user', 'updated', 'suggestion', 'ignored')
	