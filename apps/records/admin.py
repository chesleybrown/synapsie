from django.contrib import admin
from apps.records.models import Record
from apps.records.forms import RecordForm

class RecordAdmin(admin.ModelAdmin):
	form = RecordForm

admin.site.register(Record)




