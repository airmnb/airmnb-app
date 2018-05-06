
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
def get_wechatusers():
	users = m.WechatUser.query.order_by(m.WechatUser.createdAt).all()
	return jsonify(users=m.WechatUser.dump(users))

@bp.route(_name + '/<openId>', methods=['GET'])
@api
@caps()
def get_wechatuser_by_openid(openId):
	user = m.WechatUser.query.filter(m.WechatUser.openId == openId).one()
	return jsonify(users=m.WechatUser.dump(user))

@bp.route(_name, methods=['POST'])
@api
@caps()
def create_wechatuser():
	new_uuid = helper.generate_new_uuid()

	wechat_user_data = MyForm(
		Field('wechatUserId', is_mandatory=True,
			default=lambda: new_uuid,
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
		]),
		Field('openId', is_mandatory=True),
		Field('avartarUrl')
	).get_data(copy=True)

	user_data = MyForm(
		Field('userId', is_mandatory=True,
			default=lambda: new_uuid,
			normalizer=helper.normalize_uuid,
			validators=[
				helper.check_uuid_is_valid,
		]),
		Field('fullName'),
		Field('gender'),
		Field('dob'),
	).get_data(copy=True)

	wechatUser = m.WechatUser(**wechat_user_data)
	user = m.User(**user_data)
	SS.add(wechatUser)
	SS.add(user)
	SS.flush()

	return jsonify(message=_('created wechat user {0} successfully'
		).format(wechatUser.id),
		wechatUser=m.WechatUser.dump(wechatUser),
		user=m.User.dump(user),
	)
