from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class TagMessages(GeneralMessages):
	
	created = dict(
		kind="created",
		title=_("Created Tag"),
		text=_("You have successfull created a tag: %(tag_name)s"),
	)
	
	deleted = dict(
		kind="deleted",
		title=_("Deleted Tag"),
		text=_("You have successfull deleted a tag: %(tag_name)s"),
	)