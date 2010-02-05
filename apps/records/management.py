from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
	from notification import models as Notification

	#def create_notice_types(app, created_models, verbosity, **kwargs):
	#	Notification.create_notice_type("record_created", _("Record Created"), _("You have successfully created a new record."))

	#signals.post_syncdb.connect(create_notice_types, sender=Notification)
else:
	print "Skipping creation of NoticeTypes as notification app not found"