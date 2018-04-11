#!/usr/bin/env python

import uuid

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
