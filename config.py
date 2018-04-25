
import logging
import os

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
	LOG_LEVEL = logging.INFO
	SECRET_KEY = 'something unique and secret'

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	LOG_LEVEL = logging.DEBUG
	GOOGLE_APP_KEY = os.environ['GOOGLE_APP_KEY']
	GOOGLE_APP_SECRET = os.environ['GOOGLE_APP_SECRET']
	GOOGLE_TOKEN_ENDPOINT = os.environ['GOOGLE_TOKEN_ENDPOINT']
	GOOGLE_AUTHORIZATION_URL = os.environ['GOOGLE_AUTHORIZATION_URL']


class StageConfig(Config):
	pass


class ProductionConfig(Config):
	pass


config = {
	'production': ProductionConfig,
	'stage': StageConfig,
	'development': DevelopmentConfig,
	'default': DevelopmentConfig,
}
