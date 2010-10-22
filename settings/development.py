import os
from settings import *
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

# Django settings for synapsie project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells django to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'dj_synapsie',						# Or path to database file if using sqlite3.
		'USER': 'dj_synapsie',						# Not used with sqlite3.
		'PASSWORD': 'syn.apsie.141',					# Not used with sqlite3.
		'HOST': '127.0.0.1',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '3308',						 # Set to empty string for default. Not used with sqlite3.
	}
}

SITE_ID = 1
SITE_DOMAIN = 'taglife.local:8000'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/site_media/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
	os.path.join(PROJECT_ROOT, 'media'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'emails')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'noreply@synapsie.com'
EMAIL_HOST_PASSWORD = 'abozv8x9d8bj'
EMAIL_USE_TLS = True


ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_PASSWORD_RESET_DAYS = 7

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'handlers': {
		'null': {
			'level':'DEBUG',
			'class':'django.utils.log.NullHandler',
		},
		'console':{
			'level':'DEBUG',
			'class':'logging.StreamHandler',
			'formatter': 'simple'
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
		}
	},
	'loggers': {
		'django': {
			'handlers':['console'],
			'propagate': True,
			'level':'INFO',
		},
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': False,
		},
	}
}