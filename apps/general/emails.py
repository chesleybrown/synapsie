from django.utils.translation import ugettext as _
from django.conf import settings

class GeneralEmails():
	
	def get(self, key, params={}):
		
		# dynamically get the requested attr
		email = getattr(self, key)
		
		# this prevents the caching issue
		custom_email = {}
		custom_email.update(email)
		
		# always supply domain
		params['SITE_DOMAIN'] = settings.SITE_DOMAIN
		
		# input vars
		custom_email['subject'] = email['subject'] % params
		custom_email['body'] = email['body'] % params
		
		return custom_email
	