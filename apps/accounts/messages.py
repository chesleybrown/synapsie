from apps.general.messages import GeneralMessages
from django.utils.translation import ugettext as _

class AccountMessages(GeneralMessages):
	
	invalid = dict(
		status=400,
		kind="error",
		title=_("Invalid Login"),
		text=_("You provided an invalid login. Dummy."),
		sticky=False,
	)
	
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
	
	activated = dict(
		status=201,
		kind="created",
		title=_("Activated Account"),
		text=_("Welcome to TagLife %(account_first_name)s %(account_last_name)s"),
		sticky=False,
	)
	
	invalid_activation_key = dict(
		status=400,
		kind="error",
		title=_("Invalid Activation Key"),
		text=_("You provided an invalid or expired activation key."),
		sticky=False,
	)
	
	created = dict(
		status=201,
		kind="created",
		title=_("Created Account"),
		text=_("We have emailed you at %(account_email)s with instructions to activate your account"),
		sticky=False,
	)
	
	deleted = dict(
		status=204,
		kind="deleted",
		title=_("Deleted Account"),
		text=_("You have successfully deleted your account, %(account_username)s"),
		sticky=False,
	)