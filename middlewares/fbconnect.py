 # FacebookConnectMiddleware.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

import cgi
import hashlib
import urllib
import time
import json as simplejson
from datetime import datetime

from apps.accounts.models import RegistrationManager, RegistrationProfile
from lib import facebook as facebook

# These values could be placed in Django's project settings
# More info here: http://nyquistrate.com/django/facebook-connect/
API_KEY = '168453549861030'
API_SECRET = '25dd90990d7444d4c8b7a5467ac6bc43'

REST_SERVER = 'http://api.facebook.com/restserver.php'

# You can get your User ID here: http://developers.facebook.com/tools.php?api
MY_FACEBOOK_UID = 'YOUR FACEBOOK User ID'

NOT_FRIEND_ERROR = 'You must be my Facebook friend to log in.'
PROBLEM_ERROR = 'There was a problem. Try again later.'
ACCOUNT_DISABLED_ERROR = 'Your account is not active.'
ACCOUNT_PROBLEM_ERROR = 'There is a problem with your account.'

class FacebookConnectMiddleware(object):
	
	delete_fb_cookies = False
	facebook_user_is_authenticated = False
	
	def process_request(self, request):
		try:
			 # Set the facebook message to empty. This message can be used to dispaly info from the middleware on a Web page.
			request.facebook_message = None
			
			# Don't bother trying FB Connect login if the user is already logged in
			if not request.user.is_authenticated():
				
				facebook_user_cookie = facebook.get_user_from_cookie(request.COOKIES, API_KEY, API_SECRET)
				
				# FB Connect will set a cookie with a key == FB App API Key if the user has been authenticated
				#if API_KEY in request.COOKIES.keys():
				if facebook_user_cookie:
					
					signature_hash = self.get_facebook_signature(facebook_user_cookie)
					
					# The hash of the values in the cookie to make sure they're not forged
					if (signature_hash == facebook_user_cookie['sig']):
						
						# If session hasn't expired
						if (datetime.fromtimestamp(float(facebook_user_cookie['expires'])) > datetime.now()):
							
							try:
								# Try to get Django account corresponding to user
								# Authenticate then login (or display disabled error message)
								#django_user = User.objects.get(facebook_id=facebook_user_cookie['uid'])
								user_registration_profile = RegistrationProfile.objects.get(facebook_id=facebook_user_cookie['uid'])
								user = user_registration_profile.user
								
								#user = authenticate(
								#	username='facebook_'+facebook_user_cookie['uid'], 
								#	password=hashlib.md5('facebook_'+facebook_user_cookie['uid'] + settings.SECRET_KEY).hexdigest()
								#)
								
								# allows me to log user in without knowing password
								user.backend = 'django.contrib.auth.backends.ModelBackend'
								
								if user is not None:
									if user.is_active:
										login(request, user)
										self.facebook_user_is_authenticated = True
									else:
										request.facebook_message = ACCOUNT_DISABLED_ERROR
										self.delete_fb_cookies = True
								else:
									request.facebook_message = ACCOUNT_PROBLEM_ERROR
									self.delete_fb_cookies = True
								
							except RegistrationProfile.DoesNotExist:
								# There is no Django account for this Facebook user.
								# Create one, then log the user in.
								
								# Make request to FB API to get user's first and last name
								user_info_params = {
									'method': 'Users.getInfo',
									'api_key': API_KEY,
									'call_id': time.time(),
									'v': '1.0',
									'uids': facebook_user_cookie['uid'],
									'fields': 'first_name,last_name,email',
									'format': 'json',
								}
								
								user_info_hash = self.get_facebook_signature(user_info_params)
								
								user_info_params['sig'] = user_info_hash
								
								user_info_params = urllib.urlencode(user_info_params)
								
								user_info_response  = simplejson.load(urllib.urlopen(REST_SERVER, user_info_params))
								
								# see if this email already exists and match it up if so
								try:
									user = User.objects.get(email=user_info_response[0]['email'])
									
									user_registration_profile = RegistrationProfile.objects.get(user=user)
									user_registration_profile.facebook_id = facebook_user_cookie['uid']
									user_registration_profile.save()
									
								except User.DoesNotExist:
									# Create user
									user = User.objects.create_user(
										'facebook_'+facebook_user_cookie['uid'],
										user_info_response[0]['email'], 
										hashlib.md5('facebook_'+facebook_user_cookie['uid'] + settings.SECRET_KEY).hexdigest()
									)
									user.first_name = user_info_response[0]['first_name']
									user.last_name = user_info_response[0]['last_name']
									
									user_registration_profile = RegistrationProfile.objects.create_profile(user)
									
									# set facebook id and save user
									user_registration_profile.facebook_id = facebook_user_cookie['uid']
									user.save()
									user_registration_profile.save()
									
									# activate
									RegistrationProfile.objects.activate_user(user_registration_profile.activation_key)
								
								# allows me to log user in without knowing password
								user.backend = 'django.contrib.auth.backends.ModelBackend'
								login(request, user)
								
								# Authenticate and log in (or display disabled error message)
								#user = authenticate(
								#	username='facebook_'+facebook_user_cookie['uid'], 
								#	password=hashlib.md5('facebook_'+facebook_user_cookie['uid'] + settings.SECRET_KEY).hexdigest()
								#)
								
								if user is not None:
									if user.is_active:
										login(request, user)
										self.facebook_user_is_authenticated = True
									else:
										request.facebook_message = ACCOUNT_DISABLED_ERROR
										self.delete_fb_cookies = True
								else:
								   request.facebook_message = ACCOUNT_PROBLEM_ERROR
								   self.delete_fb_cookies = True
							
						# Cookie session expired
						else:
							logout(request)
							self.delete_fb_cookies = True
						
					# Cookie values don't match hash
					else:
						logout(request)
						self.delete_fb_cookies = True
					
			# Logged in
			else:
				# If FB Connect user
				if API_KEY in request.COOKIES:
					# IP hash cookie set
					if 'fb_ip' in request.COOKIES:
						
						try:
							real_ip = request.META['HTTP_X_FORWARDED_FOR']
						except KeyError:
							real_ip = request.META['REMOTE_ADDR']
						
						# If IP hash cookie is NOT correct
						if request.COOKIES['fb_ip'] != hashlib.md5(real_ip + API_SECRET + settings.SECRET_KEY).hexdigest():
							 logout(request)
							 self.delete_fb_cookies = True
					# FB Connect user without hash cookie set
					else:
						logout(request)
						self.delete_fb_cookies = True
						
		# Something else happened. Make sure user doesn't have site access until problem is fixed.
		except:
			request.facebook_message = PROBLEM_ERROR
			logout(request)
			self.delete_fb_cookies = True
		
	# I don't think this is used....
	def process_response(self, request, response):        
		
		# Delete FB Connect cookies
		# FB Connect JavaScript may add them back, but this will ensure they're deleted if they should be
		if self.delete_fb_cookies is True:
			response.delete_cookie('fbs_'+API_KEY)
		
		self.delete_fb_cookies = False
		
		if self.facebook_user_is_authenticated is True:
			try:
				real_ip = request.META['HTTP_X_FORWARDED_FOR']
			except KeyError:
				real_ip = request.META['REMOTE_ADDR']
			response.set_cookie('fb_ip', hashlib.md5(real_ip + API_SECRET + settings.SECRET_KEY).hexdigest())
		
		# process_response() must always return a HttpResponse
		return response
	
	# Generates signatures for FB requests/cookies
	def get_facebook_signature(self, values_dict, is_cookie_check=False):
		signature_keys = []
		
		for key in sorted(values_dict.keys()):
			if (is_cookie_check and key.startswith(API_KEY + '_')):
				signature_keys.append(key)
			elif (is_cookie_check is False):
				if key != 'sig':
					signature_keys.append(key)
		
		if is_cookie_check:
			signature_string = ''.join(['%s=%s' % (x.replace(API_KEY + '_',''), values_dict[x]) for x in signature_keys])
		else:
			signature_string = ''.join(['%s=%s' % (x, values_dict[x]) for x in signature_keys])
		
		signature_string = signature_string + API_SECRET
		
		return hashlib.md5(signature_string).hexdigest()