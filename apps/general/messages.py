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
			custom_message['text'] = message['text'] % params
		
		return custom_message
	
	unknown_error = dict(
		status=500,
		kind="error",
		title=_("Unknown Error"),
		text=_("Something seriously broke... Rare, I know. Sorry."),
		sticky=False,
	)
	
	permission_denied = dict(
		status=401,
		kind="error",
		title=_("Permission Denied"),
		text=_("Back off! Get your own sandwich! But really, you're not permitted to perform this action."),
		sticky=False,
	)