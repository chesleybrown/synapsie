from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class AccountMessages(GeneralMessages):
	
	logged_in = dict(
		status=200,
		kind="success",
		title=_("Logged In"),
		text=_("You have successfully logged in as %(account_username)s"),
		sticky=False,
	)
	
	logged_out = dict(
		status=200,
		kind="success",
		title=_("Logged Out"),
		text=_("You have successfully logged out"),
		sticky=False,
	)
	
	created = dict(
		status=201,
		kind="created",
		title=_("Created Account"),
		text=_("Welcome to TagLife %(account_username)s"),
		sticky=False,
	)
	
	deleted = dict(
		status=204,
		kind="deleted",
		title=_("Deleted Account"),
		text=_("You have successfully deleted your account, %(account_username)s"),
		sticky=False,
	)