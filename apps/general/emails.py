from django.utils.translation import ugettext as _

class GeneralEmails():
	
	def get(self, key, params=None):
		
		# dynamically get the requested attr
		email = getattr(self, key)
		
		# this prevents the caching issue
		custom_email = {}
		custom_email.update(email)
		
		# input vars
		if not params == None:
			custom_email['subject'] = email['subject'] % params
			custom_email['body'] = email['body'] % params
		
		return custom_email
	