#!/usr/bin/env python

import re
import os
import requests
import json

from flask import Flask, request, redirect, make_response, g

from config import config
from db import database as db


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)

	public_url_patterns = map(re.compile, [
		'/static/',
		'/favicon.ico',
		'/logout',
		'/authorization_response',
		'/health-check',
	])
	json_url_patterns = map(re.compile, [
		'/whoami',
		'/api'
	])

	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')


	@app.before_request
	def authenticate_request():
		for p in public_url_patterns:
			if p.match(request.path):
				return None
		# TODO: authenticate incoming request
		# if authenticated, set g.current_user and return None
		g.current_user = object()
		return None


	@app.route('/logout')
	def logout():
		return redirect(location='/')


	@app.route('/authorization_response')
	def authorization_response():
		original_url = request.args['r']
		response = redirect(location=original_url)
		return response


	@app.route('/health-check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})

	@app.route('/sso/wechat/login')
	def wechat_login():
		# https://developers.weixin.qq.com/miniprogram/dev/api/api-login.html#wxloginobject
		code = request.args['code']
		app_id = os.environ['WECHAT_APP_ID']
		secret = os.environ['WECHAT_APP_SECRET']
		url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(app_id, secret, code)
		response = requests.get(url)
		if(response.ok):
			jdata = json.loads(response.content)
			print 'debug wechat response'
			print jdata
			if(jdata.errcode == 0):
				return make_response(jdata.data.openid, 200, {'Content-Type': 'text/plain'})

		return make_response(response, 400)
	return app
