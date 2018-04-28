#!/usr/bin/env python

import os
import re
import logging
import datetime

import sqlalchemy.orm.exc
from flask import Flask, request, redirect, make_response, g, send_file, url_for, jsonify
from flask_oauthlib.client import OAuth
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

	public_url_patterns = list(map(re.compile, [
		'/static/',
		'/favicon.ico$',
		'/login$',
		'/logout$',
		'/debug$',
		'/authorization_response$',
		'/health-check$',
		'/$',
	]))
	json_url_patterns = list(map(re.compile, [
		'/whoami$',
		'/api/'
	]))


	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')

	oauth = OAuth()


	google = oauth.remote_app('google',
		base_url=None,
		request_token_url=None,
		access_token_url=app.config['AMB_GOOGLE_ACCESS_TOKEN_URL'],
		authorize_url=app.config['AMB_GOOGLE_AUTHORIZE_URL'],
		consumer_key=app.config['AMB_GOOGLE_APP_KEY'],
		consumer_secret=app.config['AMB_GOOGLE_APP_SECRET'],
		request_token_params={'scope': 'openid email profile', 'state': 'google'},
	)

	facebook = oauth.remote_app('facebook',
		base_url='https://graph.facebook.com/',
		request_token_url=None,
		access_token_url=app.config['AMB_FACEBOOK_ACCESS_TOKEN_URL'],
		authorize_url=app.config['AMB_FACEBOOK_AUTHORIZE_URL'],
		consumer_key=app.config['AMB_FACEBOOK_APP_KEY'],
		consumer_secret=app.config['AMB_FACEBOOK_APP_SECRET'],
		request_token_params={'scope': 'email', 'state': 'facebook'}
	)


	@app.before_request
	def authenticate_request():
		for i, p in enumerate(public_url_patterns):
			if p.match(request.path):
				return None

		try:
			if 'authoization' not in request.headers:
				raise RuntimeError('Authorization header not found for non-public url: {}'.format(request.path))
			if not auth_header.startswith('Bearer '):
				raise RuntimeError('Authorization header not valid: {}'.format(auth_header))
			token = auth_header[7:]
			try:
				payload = jwt.decode(token, os.environ.get('SECRET') or '')
				userId = payload['userId']
				expires = datetime.datetime.strpfmt(payload['expires'], '%Y-%m-%dT%H:%M:%S%z')
			except:
				raise RuntimeError('Authorization header not valid: {}'.format(auth_header))
			now = datetime.datetime.now()
			if expires < now:
				# session expires
				raise ValueError('session expired at {}, now {}'.format(expires, now))
			user = m.User.query.get(m.User.userId==userId)
			if user:
				# authentication succeeded
				g.current_user = user
				return None

		except Exception as e:
			# authentication failed
			print('authentication failed: {}'.format(e))
			print('request.path', request.path)
			if request.path == '/whoami':
				# create a new session
				print('requesting /whoami but authentication failed, about to create a new one');
				three_days_later = datetime.datetime.now() + datetime.timedelta(days=3)
				ses = m.Session(sessionExpiresAt=three_days_later)
				SS.add(ses)
				SS.commit()
				return make_response(jsonify(session=m.Session.dump(ses)),
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

	@app.route('/authorization_response')
	def authorization_response():
		state = request.args.get('state', '')
		if state.find('google') >= 0:
			provider = google
		elif state.find('facebook') >= 0:
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

		# TODO: create jwt token for user
		return redirect(location='/debug')


	@app.route('/debug')
	def debug():
		buf = []
		for k, v in sorted(os.environ.items()):
			buf.append('{}\t{}\n'.format(k, v))
		return make_response(('\n'.join(buf), {'Content-Type': 'application/json'}))


	@app.route('/health-check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})


	@app.route('/login')
	def login():
		identity_provider = request.args.get('use', '')

		if identity_provider == 'google':
			log.debug('login with google')
			callback = url_for('authorization_response', r=request.url, _external=True)
			# TODO: setup google.request_token_params here to include redirection url here
			callback = url_for('authorization_response', _external=True)
			return google.authorize(callback=callback)
		elif identity_provider == 'facebook':
			log.debug('loging with facebook')
			callback = url_for('authorization_response', _external=True)
			return facebook.authorize(callback=callback)
		return 'you are logged in'


	@app.route('/logout')
	def logout():

		return redirect(location='/')

	@app.route('/whoami')
	def whoami():
		return jsonify(sessionId='123', accessToken='access', refreshToken='refresh', userId='unknown')

	@app.route('/', defaults={'path': ''})
	@app.route('/<path:path>')
	def catch_all(path):
		return send_file('index.html', cache_timeout=0)

	return app
