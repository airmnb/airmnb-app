
from flask import request, session, jsonify

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
def get_users():
	users = m.User.query.order_by(m.User.createdAt).all()
	return jsonify(users=m.User.dump(users))


@bp.route(_name + '/<userId>', methods=['GET'])
@api
@caps()
def get_user(userId):
	user = m.User.query.filter(m.User.userId == userId).one()
	return jsonify(user=m.User.dump(user))


@bp.route(_name + '/<userId>', methods=['PUT'])
@api
@caps()
def update_user(userId):
	user = m.User.query.get(userId)
	if not user:
		raise InvalidUsage(_('user {0} not found').format(userId), 404)
	data = MyForm(
		Field('accountName'),
		Field('fullName'),
		Field('gender'),
		Field('dob'),
		Field('email'),
		Field('phone'),
	).get_data()
	for k, v in data.items():
		setattr(user, k, v)
	SS.flush()
	return jsonify(
		message=_('Updated user {0} successfully').format(userId),
		user=m.User.dump(user),
	)
