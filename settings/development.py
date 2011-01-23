import os
from settings import *
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

# Django settings for synapsie project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells django to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

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

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'middlewares.ssl.SSLRedirect',
	'middlewares.fbconnect.FacebookConnectMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware', # need debug
)

# Debugging
INTERNAL_IPS = (
	'127.0.0.1',
)
DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'HIDE_DJANGO_SQL': False,
}

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	
	# synapsie
	'apps.accounts',
	'apps.about',
	'apps.session_messages',
	'piston',
	'compress',
	'apps.general',
	'apps.records',
	'apps.tags',
	'tagging',
	
	# debug
	'debug_toolbar',
)

SITE_DOMAIN = 'taglife.local:8000'

# compression disabled for development
COMPRESS = False
COMPRESS_CSS_FILTERS = None

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'emails')

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