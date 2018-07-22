import os

from flask import request, session, jsonify, g

import datetime
from dateutil.tz import tzoffset
import db.model as m
from db import database as db
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]


@bp.route(_name, methods=['GET'])
@api
@caps()
def get_favorite():
	# Get consumer's favorites
	user = g.current_user	
	consumerId = user.userId	
	favorites = m.Favorite.query.filter(m.Favorite.consumerId == consumerId).all()
	return jsonify(favorites=m.Favorite.dump(favorites))


@bp.route(_name, methods=['POST'])
@api
@caps()
def create_favorite():
	user = g.current_user	
	data = MyForm(
		Field('activityId', is_mandatory=True, validators=[
			helper.check_uuid_is_valid,
		]),
		Field('providerId', is_mandatory=True, validators=[
			helper.check_uuid_is_valid,
		]),
		Field('consumerId', is_mandatory=True, default=user.userId, validators=[
			helper.check_uuid_is_valid,
		]),
		).get_data()
	#
	# TODO: check if user (userId) is a consumer of activity (activityId)
	#
	favorite = m.Favorite(**data)
	SS.add(favorite)
	SS.flush()
	return jsonify(message=_('successfully created favorite {}').format(favorite.favoriteId),
		favorite=m.Favorite.dump(favorite),
		)


@bp.route(_name + '/<favoriteId>', methods=['DELETE'])
@api
@caps()
def delete_favorite(favoriteId):
	favorite = m.Favorite.query.get(favoriteId)
	if not favorite:
		raise InvalidUsage(_('Favorite {0} not found').format(favoriteId), 404)

	# TODO: check other dependencies
	SS.delete(favorite)
	return jsonify(message=_('Favorite {0} was deleted successfully'
		).format(favoriteId))

