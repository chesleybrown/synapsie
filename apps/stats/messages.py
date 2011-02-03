from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class StatMessages(GeneralMessages):
	
	missing_data = dict(
		status=400,
		kind="error",
		title=_("Missing Information"),
		text=_("Did you even submit anything? Or maybe something is invalid?"),
		sticky=False,
	)
	
	not_found = dict(
		status=404,
		kind="error",
		title=_("Stat Not Found"),
		text=_("Honestly. We really couldn't find it."),
		sticky=False,
	)
	
	found = dict(
		status=200,
		kind="success",
		title=_("Stat Found"),
		text=_("The requested stat was found."),
		sticky=False,
	)
	