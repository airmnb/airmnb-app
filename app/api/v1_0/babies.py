
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
def get_babies():
	babies = m.Baby.query.order_by(m.Baby.createdAt).all()
	return jsonify(babies=m.Baby.dump(babies))

@bp.route(_name, methods=['POST'])
@api
@caps()
def add_baby():
	data = MyForm(
		Field('avatarImageId'),
		Field('nickName'),
		Field('fullName'),
		Field('gender'),
		Field('dob'),
		Field('info'),
		Field('creatorId'),
	).get_data()

	baby = m.Baby()
	for k, v in data.items():
		setattr(baby, k, v)
	
	if baby.avatarImageId:
		image = m.Image.query.get(baby.avatarImageId)
		if image:
			image.linked = True

	SS.add(baby)
	SS.flush()

	return jsonify(
		message=_('Creating baby {0} successfully').format(baby.babyId),
		baby=m.Baby.dump(baby),
	)


@bp.route(_name + '/<babyId>', methods=['GET'])
@api
@caps()
def get_baby(babyId):
	baby = m.Baby.query.filter(m.Baby.babyId == babyId).one()
	return jsonify(baby=m.Baby.dump(baby))


@bp.route(_name + '/<babyId>', methods=['PUT'])
@api
@caps()
def update_baby(babyId):
	baby = m.Baby.query.get(babyId)
	if not baby:
		raise InvalidUsage(_('baby {0} not found').format(babyId), 404)
	data = MyForm(
		Field('avatarImageId'),
		Field('nickName'),
		Field('fullName'),
		Field('gender'),
		Field('dob'),
		Field('info'),
		Field('creatorId'),
	).get_data()
	for k, v in data.items():
		setattr(baby, k, v)
	SS.flush()
	return jsonify(
		message=_('Updating baby {0} successfully').format(babyId),
		baby=m.Baby.dump(baby),
	)
