from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class RecordMessages(GeneralMessages):
	
	created = dict(
		status="added",
		title=_("Created Record"),
		desc=_("You have successfully created a record: %(record_text)s"),
	)
	
	deleted = dict(
		status="removed",
		title=_("Deleted Record"),
		desc=_("You have successfully deleted a record: %(record_text)s"),
	)