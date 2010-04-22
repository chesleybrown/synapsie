from django import forms
from apps.records.models import Record
from tagging.forms import TagField
from datetime import date, datetime
from django.utils.translation import ugettext_lazy as _

class RecordForm(forms.ModelForm):
	text = forms.CharField(label=_('Life Record...'), widget=forms.Textarea(
		attrs={'class': 'text use_elastic'}
	))
	tags = TagField(label=_('Tags for Life Record...'), widget=forms.SelectMultiple, required=False)
	personal = forms.CharField(widget=forms.HiddenInput(), initial='1')
	date = forms.CharField(widget=forms.HiddenInput, initial=date.today())
	hour = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%I"))
	minute = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%M"))
	ampm = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%p"))
	datetime_set = forms.CharField(widget=forms.HiddenInput, initial=0)
	
	def clean_personal(self):
		personal = int(self.cleaned_data['personal'])
		
		return personal
	
	def __init__(self, *args, **kwrds):
		super(RecordForm, self).__init__(*args, **kwrds)
		self.fields['tags'].widget.attrs['value'] = self.instance.get_tags_printable()

	class Meta:
		model = Record
		exclude = ('created', 'user')

class RecordAddTagsForm(forms.ModelForm):
	tags = TagField(label=_('Tags for Life Record...'), widget=forms.SelectMultiple, required=False)
	
	def __init__(self, *args, **kwrds):
		super(RecordAddTagsForm, self).__init__(*args, **kwrds)
		self.fields['tags'].widget.attrs['value'] = self.instance.get_tags_printable()

	class Meta:
		model = Record
		exclude = ('text', 'created', 'user', 'personal')

class RecordSearchForm(forms.ModelForm):
	text = forms.CharField(label=_('Search Your Life...'))
	tags = TagField(label='Filter by Tags...', widget=forms.SelectMultiple, required=False)
	
	def __init__(self, *args, **kwrds):
		super(RecordSearchForm, self).__init__(*args, **kwrds)
		self.fields['tags'].widget.attrs['value'] = self.instance.get_tags_printable()

	class Meta:
		model = Record
		exclude = ('created', 'user')