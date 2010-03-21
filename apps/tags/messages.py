from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class TagMessages(GeneralMessages):
	
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