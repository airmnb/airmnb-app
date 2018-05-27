
from flask import request, session, jsonify, g

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name, methods=['GET'])
@api
@caps()
def get_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.providerId == user.userId).order_by(m.Activity.name).all()
	return jsonify(activities=m.Activity.dump(activities))

@bp.route(_name + '/ongoing', methods=['GET'])
@api
@caps()
def get_ongoing_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.providerId == user.userId and m.Activity.status == 0).order_by(m.Activity.name).all()
	activityJsons = m.Activity.dump(activities)
	return jsonify(activities=activityJsons)

@bp.route(_name + '/closed', methods=['GET'])
@api
@caps()
def get_closed_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.providerId == user.userId and m.Activity.status != 0).order_by(m.Activity.name).all()
	return jsonify(activities=m.Activity.dump(activities))

@bp.route(_name + '/recommended', methods=['GET'])
@api
@caps()
def get_recommended_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.status == 0).order_by(m.Activity.name).limit(10).all()
	activityJsons = m.Activity.dump(activities)
	return jsonify(activities=activityJsons)

def check_uuid_availability(data, key, activityId):
	if m.Activity.query.get(activityId):
		raise ValueError(_('activityId \'{0}\' is already in use').format(activityId))


def check_venue_existence(data, key, venueId):
	if not m.Venue.query.get(venueId):
		raise ValueError(_('venue \'{0}\' is not found').format(venueId))

def check_image_ids(data, key, imageIds):
	for i in imageIds:
		if not m.Image.query.get(i):
			raise ValueError(_('image \'{0}\' is not found').format(i))

@bp.route(_name, methods=['POST'])
@api
@caps()
def create_new_activity():
	
	data = MyForm(
		Field('name', is_mandatory=True, validators=[
			validators.non_blank,
			]),
		Field('info'),
		Field('venueId', is_mandatory=True,
			validators=[
				helper.check_uuid_is_valid,
				check_venue_existence,
			]),
		Field('providerId', is_mandatory=True, default=lambda: g.current_user.userId),
		Field('gender'),
		Field('price'),
		Field('currency'),
		Field('capacity', validators=[
			# validators.is_number, (), dict(min_value=1)
			]),
		Field('startDate', is_mandatory=False, ),
			# normalizers=[
			# 	helper.normalize_date,
			# ]),
		Field('endDate', is_mandatory=False, ),
			# normalizers=[
			# 	helper.normalize_date,
			# ]),
		Field('startTime', is_mandatory=True, ),
			# normalizers=[
			# 	helper.normalize_time,
			# ]),
		Field('endTime', is_mandatory=True, ),
			# normalizers=[
			# 	helper.normalize_time,
			# ]),
		Field('imageIds', is_mandatory=False, validators=[
			check_image_ids,
			]),
		Field('daysOfWeek', is_mandatory=False, ),
			# normalizers=[
			# 	helper.normalize_week_day_mask
			# ]),
	).get_data(copy=True)

	startDate = data.pop('startDate')
	endDate = data.pop('endDate')
	startTime = data.pop('startTime')
	endTime = data.pop('endTime')
	imageIds = data.pop('imageIds')
	daysOfWeek = data.pop('daysOfWeek')

	activity = m.Activity(**data)
	SS.add(activity)
	SS.flush()

	return jsonify(message=_('created activity {0} successfully'
		).format(activity.activityId),
		activity=m.Activity.dump(activity),
	)

@bp.route(_name + '/<activityId>', methods=['GET'])
@api
@caps()
def get_activity(activityId):
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)
	return jsonify(activity=m.Activity.dump(activity))


@bp.route(_name + '/<activityId>', methods=['DELETE'])
@api
@caps()
def delete_activity(activityId):
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)

	# TODO: check other dependencies
	SS.delete(activity)
	return jsonify(message=_('activity {0} was deleted successfully'
		).format(activityId))

