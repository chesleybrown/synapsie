from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class TagMessages(GeneralMessages):
	
	not_found = dict(
		status=404,
		kind="error",
		title=_("Tag Not Found"),
		text=_("Honestly, we couldn't find the tag you were looking for."),
		sticky=False,
	)
	
	invalid = dict(
		status=400,
		kind="error",
		title=_("Invalid Tag"),
		text=_("What you provided wasn't very valid."),
		sticky=False,
	)
	
	updated = dict(
		status=200,
		kind="success",
		title=_("Updated Tag"),
		text=_("You have successfull updated a tag: %(tag_name)s"),
		sticky=False,
	)
	
	created = dict(
		status=201,
		kind="created",
		title=_("Created Tag"),
		text=_("You have successfull created a tag: %(tag_name)s"),
		sticky=False,
	)
	
	deleted = dict(
		status=204,
		kind="deleted",
		title=_("Deleted Tag"),
		text=_("You have successfull deleted a tag: %(tag_name)s"),
		sticky=False,
	)