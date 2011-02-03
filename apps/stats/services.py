from __future__ import division
from utils import odict
import datetime
import time

from django.contrib.auth.models import User

import apps.records.models
import apps.accounts.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


# weekly stats
def get_weekly(request, user=None, weeks=4, all_time=False):
	
	# init
	identity = request.user
	today = datetime.date.today()
	weeks_ago = today - datetime.timedelta(weeks=weeks)
	weekly_results = odict.OrderedDict([
		('Sunday', list()),
		('Monday', list()),
		('Tuesday', list()),
		('Wednesday', list()),
		('Thursday', list()),
		('Friday', list()),
		('Saturday', list()),
	])
	final_weekly_results = list()
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	records = (
		apps.records.models.Record.objects
		.only('id', 'quality', 'happened')
		.exclude(quality__isnull=True)
	)
	
	# retrieve all the user's records
	if all_time:
		records = records.filter(user=user)
	
	# retrieve all the user's records from the past weeks
	else:
		records = records.filter(user=user, happened__gte=weeks_ago)
	
	# split results into each day of the week
	for record in records:
		
		if record.happened.weekday() == 6:
			weekly_results['Sunday'].append(record)
		
		elif record.happened.weekday() == 0:
			weekly_results['Monday'].append(record)
		
		elif record.happened.weekday() == 1:
			weekly_results['Tuesday'].append(record)
		
		elif record.happened.weekday() == 2:
			weekly_results['Wednesday'].append(record)
		
		elif record.happened.weekday() == 3:
			weekly_results['Thursday'].append(record)
		
		elif record.happened.weekday() == 4:
			weekly_results['Friday'].append(record)
		
		elif record.happened.weekday() == 5:
			weekly_results['Saturday'].append(record)
		
	
	# average out the quality of each weekday
	for weekday, records in weekly_results.items():
		
		quality = 0
		average_quality = None
		
		for record in records:
			quality = quality + record.quality
		
		if len(records) > 0 and quality > 0:
			average_quality = round(quality / len(records), 1)
		
		final_weekly_results.append({
			'weekday': weekday,
			'quality': average_quality,
		})
	
	return final_weekly_results
