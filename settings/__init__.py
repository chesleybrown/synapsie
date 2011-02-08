import os
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

# Django settings for synapsie project.

DEBUG = False
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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/St_Johns'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_DOMAIN = 'www.synapsie.com'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

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

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=h*)f311++wt=e55rm0#(*#=y!abozv8x9d8bj+v1!gnxgvv%-'

# Context processors for templates
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	
	# synapsie
	"apps.session_messages.context_processors.session_messages",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'middlewares.ssl.SSLRedirect',
	'middlewares.fbconnect.FacebookConnectMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, "templates"),
)

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
	'apps.stats',
	'apps.suggestions',
	'tagging',
)

# tagging settings
FORCE_LOWERCASE_TAGS = True
MAX_TAG_LENGTH = 50

# compressed CSS and JS
COMPRESS = True
COMPRESS_AUTO = True
COMPRESS_VERSION = True
CSSTIDY_BINARY = '/usr/bin/csstidy'
COMPRESS_CSS_FILTERS = None
COMPRESS_CSS = {
	'marketing': {
		'source_filenames': (
			'media/css/reset.css',
			'media/css/960.css',
			'media/css/text.css',
			'media/css/base.css',
			'media/css/marketing.css',
			'media/css/buttons.css',
			'media/css/tabs.css',
			'media/css/icons.css',
			'media/css/message_box.css',
			'media/css/polaroids.css',
			'media/css/records.css',
			'media/css/tags.css',
			'media/css/user_voice.css',
			'media/css/jquery.gritter.css',
		),
		'output_filename': 'media/css/min/marketing.r?.css',
	},
	'app': {
		'source_filenames': (
			'media/css/reset.css',
			'media/css/960.css',
			'media/css/text.css',
			'media/css/base.css',
			'media/css/dropdown_menu.css',
			'media/css/buttons.css',
			'media/css/records.css',
			'media/css/suggestions.css',
			'media/css/tabs.css',
			'media/css/charts.css',
			'media/css/icons.css',
			'media/css/message_box.css',
			'media/css/tags.css',
			'media/css/user_voice.css',
			'media/css/jquery.datePicker.css',
			'media/css/jquery.gritter.css',
		),
		'output_filename': 'media/css/min/app.r?.css',
	}
}
COMPRESS_JS = {
	'site': {
		'source_filenames': (
			'media/js/lib/min/jquery-1.5.min.js',
			'media/js/lib/date.js',
			'media/js/plugins/jquery.fcbkcomplete.js',
			'media/js/custom/jquery.base.js',
			'media/js/custom/jquery.dropdown_menus.js',
			'media/js/custom/jquery.tabs.js',
			'media/js/custom/jquery.stats.js',
			'media/js/custom/jquery.facebook.js',
			'media/js/plugins/jquery.form-2.36.js',
			'media/js/plugins/jquery.infieldlabel.js',
			'media/js/plugins/jquery.elastic.js',
			'media/js/plugins/jquery.timeago.js',
			'media/js/plugins/jquery.blockUI.js',
			'media/js/plugins/jquery.datePicker.js',
			'media/js/plugins/jquery.highlight.js',
			'media/js/plugins/jquery.gritter.js',
			'media/js/plugins/jquery.ezpz_hint.js',
			'media/js/custom/jquery.gritter_extend.js',
			'media/js/custom/jquery.sidebar.js',
			'media/js/custom/loader.uservoice.js',
		),
		'output_filename': 'media/js/min/site.r?.js',
	}
}

DEFAULT_TAGS = [
	{'name': 'april fool\'s'},
	{'name': 'awkward'},
	{'name': 'bad'},
	{'name': 'birthday'},
	{'name': 'broken'},
	{'name': 'busniness'},
	{'name': 'camping'},
	{'name': 'cars'},
	{'name': 'christmas'},
	{'name': 'concert'},
	{'name': 'crazy'},
	{'name': 'cute'},
	{'name': 'dating'},
	{'name': 'depressing'},
	{'name': 'drinking'},
	{'name': 'early'},
	{'name': 'easter'},
	{'name': 'entertainment'},
	{'name': 'event'},
	{'name': 'fail'},
	{'name': 'family'},
	{'name': 'father\'s day'},
	{'name': 'financial'},
	{'name': 'first'},
	{'name': 'fml'},
	{'name': 'food'},
	{'name': 'free'},
	{'name': 'friends'},
	{'name': 'fun'},
	{'name': 'games'},
	{'name': 'girls'},
	{'name': 'goals'},
	{'name': 'good'},
	{'name': 'gym'},
	{'name': 'halloween'},
	{'name': 'happy'},
	{'name': 'hate'},
	{'name': 'holiday'},
	{'name': 'home'},
	{'name': 'hope'},
	{'name': 'hot'},
	{'name': 'idea'},
	{'name': 'interesting'},
	{'name': 'kiss'},
	{'name': 'lame'},
	{'name': 'last'},
	{'name': 'late night'},
	{'name': 'lazy'},
	{'name': 'lie'},
	{'name': 'love'},
	{'name': 'lucky'},
	{'name': 'mother\'s day'},
	{'name': 'movies'},
	{'name': 'nightmare'},
	{'name': 'new year\'s'},
	{'name': 'painful'},
	{'name': 'party'},
	{'name': 'pets'},
	{'name': 'random'},
	{'name': 'regret'},
	{'name': 'sad'},
	{'name': 'sex'},
	{'name': 'sick'},
	{'name': 'stupid'},
	{'name': 'st. patrick\'s day'},
	{'name': 'surprise'},
	{'name': 'taxes'},
	{'name': 'thanksgiving'},
	{'name': 'theatres'},
	{'name': 'tv'},
	{'name': 'vacation'},
	{'name': 'valentine\'s day'},
	{'name': 'walk'},
	{'name': 'wild'},
	{'name': 'wishlist'},
	{'name': 'work'},
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
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