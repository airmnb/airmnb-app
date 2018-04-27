
from flask import request, session, jsonify, make_response

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage
import os
import requests
import json

from . import _helper as helper

_name = __file__.split('/')[-1].split('.')[0]


@bp.route(_name + '/wechat/login', methods=['GET'])
@api
@caps()
def wechat_login():
	# https://developers.weixin.qq.com/miniprogram/dev/api/api-login.html#wxloginobject
		code = request.args['code']
		app_id = os.environ['AMB_WECHAT_APP_ID']
		secret = os.environ['AMB_WECHAT_APP_SECRET']
		url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(app_id, secret, code)
		response = requests.get(url)
		if(response.ok):
			jdata = json.loads(response.content)
			if(not 'errcode' in jdata):
				openid = jdata['openid']
				# TOOD: Add logic to get_or_set AirMnb profile
				wechat_user = m.WechatUser.query.filter(m.WechatUser.openId == openid).one_or_none()
				if(wechat_user is None):
					userid = str(helper.generate_new_uuid())
					wechat_user = m.WechatUser(**{
						'id': userid, 
						'openId': openid,
					})
					user = m.User(**{
						'id': userid,
					})
					SS.add(wechat_user)
					SS.add(user)
					SS.flush()
				else:
					user = m.User.query.filter(m.User.id == wechat_user.id).one()
				return jsonify(user=m.User.dump(user))

		return make_response('Bad request', 400)
