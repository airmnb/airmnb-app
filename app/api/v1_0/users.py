
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name + '/', methods=['GET'])
@api
@caps()
def get_users():
	users = m.User.query.order_by(m.User.createdAt).all()
	return jsonify(users=m.User.dump(users))

@bp.route(_name + '/<userId>', methods=['GET'])
@api
@caps()
def get_user(userId):
	user = m.User.query.filter(m.User.userId == userId).one()
	return jsonify(users=m.User.dump(user))

@bp.route(_name + '/', methods=['PUT'])
@api
@caps()
def update_user():
	data = MyForm(
		Field('id', is_mandatory=True,
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
		]),
		Field('full_name'),
		Field('gender'),
		Field('dob'),
	).get_data(copy=True)

	user = m.User(**data)
	SS.add(user)
	SS.flush()

	return jsonify(message=_('Updated user {0} successfully'
		).format(user.id),
		user=m.User.dump(user),
	)
