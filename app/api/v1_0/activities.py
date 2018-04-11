
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

import _helper as helper

_name = __file__.split('/')[-1].split('.')[0]


@bp.route(_name + '/', methods=['GET'])
@api
@caps()
def get_activities():
	activities = m.Activity.query.order_by(m.Activity.name).all()
	return jsonify(activities=m.Activity.dump(activities))


def check_uuid_availability(data, key, activityId):
	if m.Activity.query.get(activityId):
		raise ValueError(_('activityId \'{0}\' is already in use').format(activityId))


def check_location_existence(data, key, locationId):
	if not m.Location.query.get(locationId):
		raise ValueError(_('location \'{0}\' is not found').format(locationId))


@bp.route(_name + '/', methods=['POST'])
@api
@caps()
def create_new_activity():
	data = MyForm(
		Field('activityId', is_mandatory=True,
			default=lambda: helper.generate_new_uuid(),
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
				check_uuid_availability,
		]),
		Field('name', is_mandatory=True, validators=[
			validators.non_blank,
		]),
		Field('description'),
		Field('locationId', is_mandatory=True,
			validators=[
				helper.check_uuid_is_valid,
				check_location_existence,
		]),
	).get_data(copy=True)

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
def get_activity():
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)
	return jsonify(activity=m.Activity.dump(activity))


@bp.route(_name + '/<activityId>', methods=['DELETE'])
@api
@caps()
def delete_activity():
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)

	# TODO: check other dependencies
	SS.delete(activity)
	return jsonify(message=_('activity {0} was deleted successfully'
		).format(activityId))
