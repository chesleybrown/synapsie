from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class SuggestionMessages(GeneralMessages):
	
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
		title=_("Suggestion Not Found"),
		text=_("Honestly. We really couldn't find it."),
		sticky=False,
	)
	
	found = dict(
		status=200,
		kind="success",
		title=_("Suggestion Found"),
		text=_("The requested suggestion was found."),
		sticky=False,
	)
	
	user_suggestion_updated = dict(
		status=200,
		kind="success",
		title=_("User Suggestion Updated"),
		text=_("The user suggestion was updated."),
		sticky=False,
	)
	
	setup_completed = dict(
		status=200,
		kind="success",
		title=_("Suggestions Updated"),
		text=_("All suggestions were updated."),
		sticky=False,
	)
	