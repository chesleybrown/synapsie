from __future__ import division
import datetime
import time

from django.contrib.auth.models import User

import apps.records.models
import apps.accounts.models
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input


# weekly stats
def get_weekly(request, user=None, weeks=4):
	
	# init
	identity = request.user
	today = datetime.date.today()
	one_week_ago = today - datetime.timedelta(weeks=weeks)
	weekly_results = dict({
		'monday': list(),
		'tuesday': list(),
		'wednesday': list(),
		'thursday': list(),
		'friday': list(),
		'saturday': list(),
		'sunday': list(),
	})
	final_weekly_results = dict({
		'monday': 0,
		'tuesday': 0,
		'wednesday': 0,
		'thursday': 0,
		'friday': 0,
		'saturday': 0,
		'sunday': 0,
	})
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# retrieve all the user's records from the past week
	records = (
		apps.records.models.Record.objects
		.only('id', 'quality', 'happened')
		.filter(user=user, happened__gte=one_week_ago)
		.order_by('-happened', '-id')
	)
	
	# split results into each day of the week
	for record in records:
		
		if record.happened.weekday() == 0:
			weekly_results['monday'].append(record)
		
		elif record.happened.weekday() == 1:
			weekly_results['tuesday'].append(record)
		
		elif record.happened.weekday() == 2:
			weekly_results['wednesday'].append(record)
		
		elif record.happened.weekday() == 3:
			weekly_results['thursday'].append(record)
		
		elif record.happened.weekday() == 4:
			weekly_results['friday'].append(record)
		
		elif record.happened.weekday() == 5:
			weekly_results['saturday'].append(record)
		
		elif record.happened.weekday() == 6:
			weekly_results['sunday'].append(record)
	
	# average out the quality of each weekday
	for weekday, records in weekly_results.items():
		
		quality = 0
		average_quality = 0
		
		for record in records:
			quality = quality + record.quality
		
		if len(records) > 0:
			average_quality = quality / len(records)
		
		final_weekly_results[weekday] = average_quality
	
	return final_weekly_results
