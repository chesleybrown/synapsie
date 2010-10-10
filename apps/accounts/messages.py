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
	
	email_not_found = dict(
		status=400,
		kind="error",
		title=_("Email Not Found"),
		text=_("The email you entered, %(account_email)s does not belong to any account."),
		sticky=False,
	)
	
	invalid_reset_key = dict(
		status=400,
		kind="error",
		title=_("Invalid Password Reset Key"),
		text=_("The password reset key you provided was invalid. You may have to generate a new one."),
		sticky=False,
	)
	
	password_reset = dict(
		status=200,
		kind="success",
		title=_("Password Reset Confirmation"),
		text=_("We have sent a password reset confirmation to %(account_email)s. Check it out."),
		sticky=False,
	)
	
	password_updated = dict(
		status=200,
		kind="success",
		title=_("Password Updated"),
		text=_("You have successfully updated your password, try logging in with it now."),
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