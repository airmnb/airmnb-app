#!/usr/bin/env python

import os
import re
import logging
import datetime
import json
import urllib
import uuid

import sqlalchemy.orm.exc
from flask import Flask, request, redirect, make_response, g, send_file, url_for, jsonify
from flask_oauthlib.client import OAuth
from flask_cors import CORS
import requests
import jwt

from config import config
from db import database as db
from .i18n import get_text as _
import db.model as m
from db.db import SS

log = logging.getLogger('app')

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)
	CORS(app, resources={'/api/1.0/*': {'origins': '*'}, '/sys/*': {'origins': '*'}})

	public_url_patterns = list(map(re.compile, [
		'/static/',
		'/public/',
		'/favicon.ico$',
		'/sys/login$',
		'/sys/login/weapp',
		'/sys/logout$',
		'/sys/debug$',
		'/sys/authorization_response$',
		'/sys/health_check$',
		'/$',
	]))
	json_url_patterns = list(map(re.compile, [
		'/sys/whoami$',
		'/api/'
	]))


	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0')

	oauth = OAuth()


	state_dict = {}	# to be propulated by login handler

	google = oauth.remote_app('google',
		base_url=None,
		request_token_url=None,
		access_token_url=app.config['AMB_GOOGLE_ACCESS_TOKEN_URL'],
		authorize_url=app.config['AMB_GOOGLE_AUTHORIZE_URL'],
		consumer_key=app.config['AMB_GOOGLE_APP_KEY'],
		consumer_secret=app.config['AMB_GOOGLE_APP_SECRET'],
		request_token_params={'scope': 'openid email profile', 'state': state_dict},
	)

	facebook = oauth.remote_app('facebook',
		base_url='https://graph.facebook.com/',
		request_token_url=None,
		access_token_url=app.config['AMB_FACEBOOK_ACCESS_TOKEN_URL'],
		authorize_url=app.config['AMB_FACEBOOK_AUTHORIZE_URL'],
		consumer_key=app.config['AMB_FACEBOOK_APP_KEY'],
		consumer_secret=app.config['AMB_FACEBOOK_APP_SECRET'],
		request_token_params={'scope': 'email', 'state': state_dict},
	)


	@app.before_request
	def authenticate_request():
		if os.environ.get('DEBUG') and request.method == 'OPTIONS':
			return make_response('', 200)

		for i, p in enumerate(public_url_patterns):
			if p.match(request.path):
				return None

		try:
			if 'authorization' not in request.headers:
				raise RuntimeError('Authorization header not found for non-public url: {}'.format(request.path))
			auth_header = request.headers['authorization']

			# DEBUG SHORTCUT
			if os.environ.get('DEBUG') == auth_header:
				ses = m.Session.query.first()
				fake_user = m.User.query.get(ses.userId)
				g.current_user = fake_user
				g.session_id = ses.sessionId
				return None

			if not auth_header.startswith('Bearer '):
				raise RuntimeError('Authorization header not valid: {}'.format(auth_header))
			token = auth_header[7:]
			print('decoded token from authoization header', token)
			try:
				payload = jwt.decode(token, os.environ.get('SECRET') or '')
				print('payload decoded from header', payload)
				sessionId = payload['sessionId']
				# userId = payload['userId']
				#expires = datetime.datetime.strpfmt(payload['expires'], '%Y-%m-%dT%H:%M:%S%z')
				ses = m.Session.query.get(sessionId)
				userId = ses.userId
			except Exception as e:
				print('Exception is', e)
				raise RuntimeError('Authorization header not valid: {}'.format(auth_header))
			if userId is None:
				raise RuntimeError('session not attached to user')
			# now = datetime.datetime.now()
			# if expires < now:
			# 	# session expires
			# 	raise ValueError('session expired at {}, now {}'.format(expires, now))
			print('Trying to get user {}'.format(userId))
			user = m.User.query.get(userId)
			print('user decoded from header: ', user.dump(user))
			if user:
				# authentication succeeded
				g.current_user = user
				g.sessionId = sessionId
				return None

		except Exception as e:
			# authentication failed
			print('authentication failed: {}'.format(e))
			print('request.path', request.path)
			if request.path == '/sys/whoami':
				# create a new session
				print('requesting /session but authentication failed, about to create a new one');
				three_days_later = datetime.datetime.now() + datetime.timedelta(days=3)
				ses = m.Session(sessionExpiresAt=three_days_later)
				SS.add(ses)
				SS.commit()
				print('Session is', ses.dump(ses))
				payload = {
					'sessionId': ses.sessionId
				}
				print('payload is', payload)
				sessionToken = jwt.encode(payload, os.environ.get('SECRET') or '').decode('utf-8')
				return make_response(jsonify(sessionToken=sessionToken, sessionId=ses.sessionId),
					401, {'Content-Type': 'application/json'})

		is_json = False
		for p in json_url_patterns:
			if p.match(request.path):
				is_json = True
			break
		else:
			is_json = (request.headers.get('HTTP-ACCEPT') or '').find('application/json') >= 0

		if is_json:
			return make_response(jsonify(error='authentication required to access requested url'), 
				401, {'Content-Type': 'application/json'})
		return redirect(location='/#/login')

	@app.route('/sys/authorization_response')
	def authorization_response():
		state_literal = request.args.get('state', '')
		print('state literal is %r' % state_literal)
		try:
			state = eval(state_literal)
		except:
			state = {}
		print('state returned from incoming request is', state)

		if state.get('provider') == 'google':
			provider = google
		elif state.get('provider') == 'facebook':
			provider = facebook


		# retrieve the access_token using code from authorization grant
		try:
			resp = provider.authorized_response()
		except Exception as e:
			return make_response(_('error getting access token: {}').format(e), 500)

		if resp is None:
			return make_response(_('You need to grant access to continue, error: {}').format(
				request.args.get('error')), 400)

		if provider == google:
			data = jwt.decode(resp['id_token'], verify=False)
			email = data['email']
			try:
				user = m.User.query.filter(m.User.email==email).one()
			except sqlalchemy.orm.exc.NoResultFound as e:
				# user does not exist, create it
				user = m.User(
					familyName=data['family_name'],
					givenName=data['given_name'],
					# gender
					# dob
					fullName=data['name'],
					email=data['email'],
				)
				SS.add(user)
				SS.commit()
		elif provider == facebook:
			token = resp['access_token']
			try:
				data = requests.get('https://graph.facebook.com/me',
					params={'fields': ','.join(['id', 'email', 'age_range', 'first_name',
							'last_name', 'gender', 'verified', 'name'])},
					headers={
						'Authorization': 'Bearer {}'.format(token)
					}).json()
			except Exception as e:
				print (e)
				pass
			print('data is', data)
			email = data['email']
			try:
				user = m.User.query.filter(m.User.email==email).one()
			except sqlalchemy.orm.exc.NoResultFound as e:
				user = m.User(
					familyName=data['last_name'],
					givenName=data['first_name'],
					fullName=data['name'],
					email=data['email'],
				)
				SS.add(user)
				SS.commit()

		# TODO: check sessionId in csae it is invalid
		sessionId = state.get('session_id')
		# update session to mark it belongs to user
		ses = m.Session.query.get(sessionId)
		ses.userId = user.userId
		SS.flush()
		SS.commit()

		# TODO: create jwt token for user
		payload = {
			'sessionId': sessionId,
			'userId': user.userId,
			'extra': {
				'data': 'whatever',
			},
		}
		token = jwt.encode(payload, os.environ.get('SECRET') or '')
		# return redirect(location=url_for('catch_all', jwt=token, _external=True))
		# return redirect(location=url_for('dashboard', jwt=token, _external=True))
		return redirect(location=url_for('catch_all', _external=True))


	@app.route('/sys/debug', methods=['OPTIONS','GET', 'POST', 'PUT', 'DELETE'])
	def debug():
		buf = []
		for k, v in sorted(os.environ.items()):
			buf.append('{}\t{}\n'.format(k, v))
		return make_response('\n'.join(buf), 200, {'Content-Type': 'text/plain'})

	@app.route('/sys/signup')
	def singup():
		return ''

	@app.route('/sys/health_check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})

	@app.route('/sys/login/weapp')
	def weapp_login():
		# https://developers.weixin.qq.com/miniprogram/dev/api/api-login.html#wxloginobject
		code = request.args['code']
		app_id = os.environ['AMB_WEAPP_APP_ID']
		secret = os.environ['AMB_WEAPP_APP_SECRET']
		url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(app_id, secret, code)
		response = requests.get(url)
		print(response.content)
		if(response.ok):
			jdata = json.loads(response.content.decode('utf-8'))
			if(not 'errcode' in jdata):
				openid = jdata['openid']
				print('weapp openid', openid)
				# TOOD: Add logic to get_or_set AirMnb profile
				wechat_user = m.WechatUser.query.filter(m.WechatUser.openId == openid).one_or_none()
				if(wechat_user is None):
					userid = str(uuid.uuid4())
					wechat_user = m.WechatUser(**{
						'wechatUserId': userid, 
						'openId': openid,
					})
					user = m.User(**{
						'userId': userid,
					})
					SS.add(wechat_user)
					SS.add(user)
					SS.flush()
				else:
					user = m.User.query.filter(m.User.userId == wechat_user.wechatUserId).one()

				userId = user.userId
				three_days_later = datetime.datetime.now() + datetime.timedelta(days=3)
				ses = m.Session(sessionExpiresAt=three_days_later, userId=userId)
				SS.add(ses)
				SS.commit()

				sessionId = ses.sessionId
				payload = {
					'sessionId': sessionId,
					'userId': userId,
					'extra': {
						'data': 'whatever',
					},
				}
				token = jwt.encode(payload, os.environ.get('SECRET') or '').decode('utf-8')
				return jsonify(sessionToken=token, sessionId=sessionId, user=m.User.dump(user))
				# return jsonify(user=m.User.dump(user))
		return make_response('Bad request', 400)


	@app.route('/public/images/<imageId>')
	def get_image(imageId):
		image = m.Image.query.get(imageId)
		if not image:
			return make_response('image not found', 404)
		return make_response(image.blob, 200, {'Content-Type': image.mimeType,
			'Content-Length': len(image.blob)})

	@app.route('/sys/login')
	def login():
		identity_provider = request.args.get('use', '')
		session_id = request.args.get('session_id', '')

		# TODO: validate session_id

		if identity_provider == 'google':
			log.debug('login with google')
			state_dict['provider'] = 'google'
			state_dict['session_id'] = session_id
			callback = url_for('authorization_response', _external=True)
			return google.authorize(callback=callback)
		elif identity_provider == 'facebook':
			log.debug('loging with facebook')
			state_dict['provider'] = 'facebook'
			state_dict['session_id'] = session_id
			callback = url_for('authorization_response', _external=True)
			return facebook.authorize(callback=callback)
		return 'login using system database'


	@app.route('/sys/logout')
	def logout():
		return redirect(location='/')


	@app.route('/sys/whoami')
	def whoami():
		userId = g.current_user.userId
		sessionId = g.sessionId
		payload = {
			'sessionId': sessionId,
			'userId': userId,
			'extra': {
				'data': 'whatever',
			},
		}
		token = jwt.encode(payload, os.environ.get('SECRET') or '').decode('utf-8')
		return jsonify(sessionToken=token, sessionId=sessionId, user=m.User.dump(g.current_user))

	# @app.errorhandler(404)
	# def default_hander(exc):
	# 	if request.path.startswith('/static'):
	# 		return make_response(
	# 			_('Sorry, the resource you have requested for is not found'),
	# 			404)
	# 	if request.path.startswith('/api/'):
	# 		return make_response(jsonify(error='requested url not found'),
	# 			404, {})
	# 	# TODO: only redirect valid urls
	# 	return redirect('/#%s' % request.path)

	@app.route('/', defaults={'path': ''})
	@app.route('/<path:path>')
	def catch_all(path):
		if not (request.path.startswith('/sys/') or request.path.startswith('/api/')) or request.path.startswith('/public/'):
			return send_file('index.html', cache_timeout=0)
		return make_response('Not found', 404)

	return app
