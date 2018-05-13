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
	# input date must be formatted as '2018-12-31T00:00:00+1000'
	timestamp = datetime.datetime.strptime('%Y-%m-%dT%H:%M:%S%z')
	return timestamp

def normalize_time(data, key, time_literal):
	timestamp = datetime.datetime.strptime('%H:%M:%S')
	return timestamp

def normalize_week_day_mask(data, key, week_day_mask):
	return ''
