from apps.general.emails import GeneralEmails
from django.utils.translation import ugettext as _

class AccountEmails(GeneralEmails):
	
	registered = dict(
		subject=_("Welcome to Synapsie, %(account_first_name)s %(account_last_name)s!"),
		body=_("You now need to activate your account by clicking here: <a href='http://%(SITE_DOMAIN)s/accounts/activate/%(account_activation_key)s'>http://%(SITE_DOMAIN)s/accounts/activate/%(account_activation_key)s</a>."),
		from_address='info@synapsie.com',
	)
	
	reset = dict(
		subject=_("Password Reset Confirmation for Synapsie"),
		body=_("Hey %(account_first_name)s %(account_last_name)s. You recently requested to reset your password, if this is true simply click here: <a href='http://%(SITE_DOMAIN)s/accounts/resetconfirmation/%(account_reset_key)s'>http://%(SITE_DOMAIN)s/accounts/resetconfirmation/%(account_reset_key)s</a>."),
		from_address='info@synapsie.com',
	)