from django.utils.translation import ugettext as _

class GeneralMessages():
	
	def get(self, key, params=None):
		
		# dynamically get the requested attr
		message = getattr(self, key)
		
		# this prevents the caching issue
		custom_message = {}
		custom_message.update(message)
		
		# input vars
		if not params == None:
			custom_message['desc'] = message['desc'] % params
		
		return custom_message
	
	permission_denied = dict(
		status="error",
		title=_("Permission Denied"),
		desc=_("You are not permitted to perform this action."),
	)