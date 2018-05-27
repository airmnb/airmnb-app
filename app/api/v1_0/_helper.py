#!/usr/bin/env python

import uuid
import datetime

from app.i18n import get_text as _

def generate_new_uuid():
	return uuid.uuid4()

def check_uuid_is_valid(data, key, uuid_literal):
	if isinstance(uuid_literal, uuid.UUID):
		return
	try:
		value = uuid.UUID(uuid_literal)
	except ValueError:
		raise ValueError(_('not a valid uuid literal {0}').format(uuid_literal))

def normalize_uuid(data, key, uuid_value):
	return str(uuid_value)

def normalize_date(data, key, date_literal):
	print('normalize_date')
	# input date must be formatted as '2018-12-31T00:00:00+1000'
	timestamp = datetime.datetime.strptime(date_literal, '%Y-%m-%d')
	return timestamp

def normalize_time(data, key, time_literal):
	timestamp = datetime.datetime.strptime('%H:%M:%S')
	return timestamp

def normalize_week_day_mask(data, key, week_day_mask):
	return ''


def enumerate_dates(start_date, end_date, days_of_week):
	mask = int(days_of_week) & 127
	week_day_bit_mask = {}
	if (isinstance(start_date, datetime.datetime)):
		start_date = start_date.date()
	if (isinstance(end_date, datetime.datetime)):
		end_date = end_date.date()
	while start_date <= end_date:
		week_day = start_date.weekday()	# mon = 0, tue = 1, ..., sun = 6
		bit_mask = week_day_bit_mask.setdefault(week_day, pow(2, week_day + 1))
		if mask & bit_mask:
			yield start_date
		start_date += datetime.timedelta(days=1)

