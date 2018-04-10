
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
def get_locations():
	locations = m.Location.query.order_by(m.Location.locationId).all()
	return jsonify(locations=m.Location.dump(locations))


def check_uuid_availability(data, key, locationId):
	if m.Location.query.get(locationId):
		raise ValueError(_('locationId \'{0}\' is already in use').format(locationId))


@bp.route(_name + '/', methods=['POST'])
@api
@caps()
def create_new_location():
	data = MyForm(
		Field('locationId', is_mandatory=True,
			default=lambda: helper.generate_new_uuid(),
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
				check_uuid_availability,
		]),
		# TODO: validate coordinates and/or other values
		Field('langitude', is_mandatory=True, default=lambda: 0),
		Field('latitude', is_mandatory=True, default=lambda: 0),
		Field('addr1', is_mandatory=True, validators=[
			validators.non_blank,
		]),
		Field('addr2'),
		Field('addr3'),
		Field('city', is_mandatory=True, default=lambda: 'fakecity',
			validators=[
				validators.non_blank,
		]),
		Field('state', is_mandatory=True, default=lambda: 'state',
			validators=[
				validators.non_blank,
		]),
		Field('country', is_mandatory=True, default=lambda: 'country',
			validators=[
				validators.non_blank,
		]),
		Field('postcode', is_mandatory=True, default=lambda: '111',
			validators=[
				validators.non_blank,
		]),
	).get_data(copy=True)

	location = m.Location(**data)
	SS.add(location)
	SS.flush()

	return jsonify(message=_('created location {0} successfully'
		).format(location.locationId),
		location=m.Location.dump(location),
	)


@bp.route(_name + '/<locationId>', methods=['GET'])
@api
@caps()
def get_location(locationId):
	location = m.Location.query.get(locationId)
	if not location:
		raise InvalidUsage(_('location {0} not found').format(loctionId), 404)
	return jsonify(location=m.Location.dump(location))

