from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class RecordMessages(GeneralMessages):
	
	missing_data = dict(
		status=400,
		kind="error",
		title=_("Missing Information"),
		text=_("Did you even submit anything?"),
		sticky=False,
	)
	
	not_found = dict(
		status=404,
		kind="error",
		title=_("Record Not Found"),
		text=_("Honestly. We really couldn't find it."),
		sticky=False,
	)
	
	no_more = dict(
		status=200,
		kind="warning",
		title=_("No More Records Remain"),
		text=_("No more records to show."),
		sticky=False,
	)
	
	more = dict(
		status=200,
		kind="success",
		title=_("More Records Remain"),
		text=_("More records remain to be shown."),
		sticky=False,
	)
	
	created = dict(
		status=201,
		kind="created",
		title=_("Created Record"),
		text=_("You have successfully created a new record."),
		sticky=False,
	)
	
	updated = dict(
		status=200,
		kind="success",
		title=_("Updated Record"),
		text=_("You have successfull updated the record."),
		sticky=False,
	)
	
	updated_tags = dict(
		status=200,
		kind="success",
		title=_("Updated Record Tags"),
		text=_("You have successfull updated the record's tags."),
		sticky=False,
	)
	
	deleted = dict(
		status=204,
		kind="deleted",
		title=_("Deleted Record"),
		text=_("You have successfully deleted the record."),
		sticky=False,
	)