from __future__ import division
from utils.odict import OrderedDict
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
	weekly_results = OrderedDict([
		('Sun', list()),
		('Mon', list()),
		('Tue', list()),
		('Wed', list()),
		('Thu', list()),
		('Fri', list()),
		('Sat', list()),
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
			weekly_results['Sun'].append(record)
		
		elif record.happened.weekday() == 0:
			weekly_results['Mon'].append(record)
		
		elif record.happened.weekday() == 1:
			weekly_results['Tue'].append(record)
		
		elif record.happened.weekday() == 2:
			weekly_results['Wed'].append(record)
		
		elif record.happened.weekday() == 3:
			weekly_results['Thu'].append(record)
		
		elif record.happened.weekday() == 4:
			weekly_results['Fri'].append(record)
		
		elif record.happened.weekday() == 5:
			weekly_results['Sat'].append(record)
		
	
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
	
# monthly stats
def get_monthly(request, user=None, all_time=False):
	
	# init
	identity = request.user
	monthly_results = OrderedDict([
		('Jan', list()),
		('Feb', list()),
		('Mar', list()),
		('Apr', list()),
		('May', list()),
		('Jun', list()),
		('Jul', list()),
		('Aug', list()),
		('Sep', list()),
		('Oct', list()),
		('Nov', list()),
		('Dec', list()),
	])
	final_monthly_results = list()
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# retrieve all the user's records
	records = (
		apps.records.models.Record.objects
		.only('id', 'quality', 'happened')
		.exclude(quality__isnull=True)
		.filter(user=user)
	)
	
	# split results into each month of the year
	for record in records:
		
		if record.happened.month == 1:
			monthly_results['Jan'].append(record)
		
		elif record.happened.month == 2:
			monthly_results['Feb'].append(record)
		
		elif record.happened.month == 3:
			monthly_results['Mar'].append(record)
		
		elif record.happened.month == 4:
			monthly_results['Apr'].append(record)
		
		elif record.happened.month == 5:
			monthly_results['May'].append(record)
		
		elif record.happened.month == 6:
			monthly_results['Jun'].append(record)
		
		elif record.happened.month == 7:
			monthly_results['Jul'].append(record)
		
		elif record.happened.month == 8:
			monthly_results['Aug'].append(record)
		
		elif record.happened.month == 9:
			monthly_results['Sep'].append(record)
		
		elif record.happened.month == 10:
			monthly_results['Oct'].append(record)
		
		elif record.happened.month == 11:
			monthly_results['Nov'].append(record)
		
		elif record.happened.month == 12:
			monthly_results['Dec'].append(record)
	
	
	# average out the quality of each month
	for month, records in monthly_results.items():
		
		quality = 0
		average_quality = None
		
		for record in records:
			quality = quality + record.quality
		
		if len(records) > 0 and quality > 0:
			average_quality = round(quality / len(records), 1)
		
		final_monthly_results.append({
			'month': month,
			'quality': average_quality,
		})
	
	return final_monthly_results
	
# yearly stats
def get_yearly(request, user=None):
	
	# init
	identity = request.user
	yearly_results = OrderedDict()
	final_yearly_results = list()
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# retrieve all the user's records
	records = (
		apps.records.models.Record.objects
		.only('id', 'quality', 'happened')
		.exclude(quality__isnull=True)
		.filter(user=user)
		.order_by('happened')
	)
	
	# split results into each year
	for record in records:
		yearly_results[record.happened.year] = list()
		
	
	for record in records:
		yearly_results[record.happened.year].append(record)
	
	# average out the quality of each year
	for year, records in yearly_results.items():
		
		quality = 0
		average_quality = None
		
		for record in records:
			quality = quality + record.quality
		
		if len(records) > 0 and quality > 0:
			average_quality = round(quality / len(records), 1)
		
		final_yearly_results.append({
			'year': year,
			'quality': average_quality,
		})
	
	return final_yearly_results
	
def get_record_counts(request, user=None):
	
	# init
	record_stats = OrderedDict([
		('Total', 0),
		('Personal', 0),
		('Shared', 0),
	])
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get all user records
	records = apps.records.models.Record.objects.all().filter(user=user)
	
	# get record stats
	record_stats['Total'] = records.count()
	record_stats['Personal'] = records.filter(personal=True).count()
	record_stats['Shared'] = records.filter(personal=False).count()
	
	return record_stats
	
def get_tag_counts(request, user=None):
	
	# init
	tag_stats = OrderedDict([
		('Total', 0),
		('Unique', 0),
		#('Average per Record', 0),
	])
	record_stats = OrderedDict([
		('Total', 0),
	])
	
	# no user provided, just use identity
	if not user:
		user = identity
	
	# get all user records
	'''
	records = apps.records.models.Record.objects.all().filter(user=user)
	record_stats['Total'] = records.count()
	'''
	
	# get tag stats
	unique_tags = Tag.objects.usage_for_model(apps.records.models.Record, filters=dict(user=user), counts=True)
	tag_stats['Unique'] = len(unique_tags)
	
	for tag in unique_tags:
		tag_stats['Total'] += tag.count
	'''
	if tag_stats['Total']:
		tag_stats['Average per Record'] = float(tag_stats['Total']) / float(record_stats['Total'])
		tag_stats['Average per Record'] = round(tag_stats['Average per Record'], 1)
	'''
	return tag_stats