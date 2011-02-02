from __future__ import division
from datetime import datetime
import time

from django.contrib.auth.models import User

import apps.records.models
import apps.accounts.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


# weekly stats
def get_weekly(self, request, user=None, week='latest'):
	
	# init
	identity = request.user
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	
	
	return False
