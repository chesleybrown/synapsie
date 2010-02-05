from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class AccountMessages(GeneralMessages):
	
	logged_in = dict(
		status="success",
		title=_("Logged In"),
		desc=_("You have successfully logged in as %(account_username)s"),
	)
	
	logged_out = dict(
		status="success",
		title=_("Logged Out"),
		desc=_("You have successfully logged out"),
	)
	
	created = dict(
		status="added",
		title=_("Created Account"),
		desc=_("Welcome to TagLife %(account_username)s"),
	)
	
	deleted = dict(
		status="removed",
		title=_("Deleted Account"),
		desc=_("You have successfully deleted your account, %(account_username)s"),
	)