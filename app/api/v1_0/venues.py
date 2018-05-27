
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]

def check_uuid_availability(data, key, venueId):
	if m.Venue.query.get(venueId):
		raise ValueError(_('venueId \'{0}\' is already in use').format(venueId))

@bp.route(_name, methods=['GET'])
@api
@caps()
def get_venues():
	providerId = request.args.get('providerId')
	if providerId:
		venues = m.Venue.query.filter(m.Venue.providerId == providerId).order_by(m.Venue.createdAt).all()
	else:
		venues = m.Venue.query.order_by(m.Venue.createdAt).all()
	return jsonify(venues=m.Venue.dump(venues))

@bp.route(_name + '/<venueId>', methods=['GET'])
@api
@caps()
def get_venue(venueId):
	venue = m.Venue.query.get(venueId)
	if not venue:
		raise InvalidUsage(_('venue {0} not found').format(venueId), 404)
	return jsonify(venue=m.Venue.dump(venue))

@bp.route(_name + '/<venueId>', methods=['DELETE'])
@api
@caps()
def delete_venue(venueId):
	venue = m.Venue.query.get(venueId)
	if not venue:
		raise InvalidUsage(_('venue {0} not found').format(venueId), 404)
	SS.delete(venue)
	return jsonify(message=_('venue {0} was deleted successfully'
		).format(venueId))

@bp.route(_name, methods=['POST'])
@api
@caps()
def create_new_venue():
	data = MyForm(
		Field('venueId', is_mandatory=True,
			default=lambda: helper.generate_new_uuid(),
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
				check_uuid_availability,
		]),
		# TODO: validate coordinates and/or other values
		# Field('longitude', is_mandatory=True, default=lambda: 0),
		# Field('latitude', is_mandatory=True, default=lambda: 0),
		Field('name', is_mandatory=False, validators=[
			validators.non_blank,
		]),
		Field('addr1', is_mandatory=True, validators=[
			validators.non_blank,
		]),
		Field('addr2'),
		Field('addr3'),
		Field('city'),
		Field('state'),
		Field('country'),
		Field('postcode'),
	).get_data(copy=True)

	venue = m.Venue(**data)
	SS.add(venue)
	SS.flush()

	return jsonify(
		message=_('created venue {0} successfully').format(venue.venueId),
		venue=m.Venue.dump(venue),
	)


@bp.route(_name + '/<venueId>', methods=['PUT'])
@api
@caps()
def update_venue(venueId):
	venue = m.Venue.query.get(venueId)
	if not venue:
		raise InvalidUsage(_('venue {0} not found').format(venueId), 404)

	data = MyForm(
		Field('name', is_mandatory=True, validators=[
			validators.non_blank,
		]),
		Field('addr1', is_mandatory=True, validators=[
			validators.non_blank,
		]),
		Field('addr2'),
		Field('addr3'),
		Field('city', is_mandatory=True, default=lambda: 'fakecity',
			validators=[
				validators.non_blank,
		]),
		Field('state', is_mandatory=False, default=lambda: 'state',
			validators=[
				validators.non_blank,
		]),
		Field('country'),
		Field('postcode'),
	).get_data(copy=True)

	for k, v in data.items():
		setattr(venue, k, v)
	SS.flush()

	return jsonify(
		message=_('Updating venue {0} successfully').format(venue.venueId),
		venue=m.Venue.dump(venue),
	)


