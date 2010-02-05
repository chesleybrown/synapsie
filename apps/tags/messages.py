from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class TagMessages(GeneralMessages):
	
	created = dict(
		status="added",
		title=_("Created Tag"),
		desc=_("You have successfull created a tag: %(tag_name)s"),
	)
	
	deleted = dict(
		status="removed",
		title=_("Deleted Tag"),
		desc=_("You have successfull deleted a tag: %(tag_name)s"),
	)