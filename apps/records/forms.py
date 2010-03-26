from django import forms
from apps.records.models import Record
from tagging.forms import TagField
from datetime import date, datetime

class RecordForm(forms.ModelForm):
	text = forms.CharField(label='Life Record...', widget=forms.Textarea(
		attrs={'class': 'text use_elastic'}
	))
	tags = TagField(label='Tags for Life Record...', widget=forms.SelectMultiple, required=False)
	personal = forms.CharField(widget=forms.HiddenInput, initial='1')
	date = forms.CharField(widget=forms.HiddenInput, initial=date.today())
	hour = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%I"))
	minute = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%M"))
	ampm = forms.CharField(widget=forms.HiddenInput, initial=datetime.today().strftime("%p"))
	datetime_set = forms.CharField(widget=forms.HiddenInput, initial=0)
	
	def __init__(self, *args, **kwrds):
		super(RecordForm, self).__init__(*args, **kwrds)
		self.fields['tags'].widget.attrs['value'] = self.instance.get_tags_printable()

	class Meta:
		model = Record
		exclude = ('created', 'user')

class RecordSearchForm(forms.ModelForm):
	text = forms.CharField(label='Search Life Records...')
	tags = TagField(label='Filter by Tags...', widget=forms.SelectMultiple, required=False)
	
	def __init__(self, *args, **kwrds):
		super(RecordSearchForm, self).__init__(*args, **kwrds)
		self.fields['tags'].widget.attrs['value'] = self.instance.get_tags_printable()

	class Meta:
		model = Record
		exclude = ('created', 'user')