
import logging
import os

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = os.environ['AMB_DATABASE_URI']
	LOG_LEVEL = logging.INFO
	SECRET_KEY = 'something unique and secret'

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	LOG_LEVEL = logging.DEBUG

	AMB_FACEBOOK_APP_KEY = os.environ['AMB_FACEBOOK_APP_KEY']
	AMB_FACEBOOK_APP_SECRET = os.environ['AMB_FACEBOOK_APP_SECRET']
	AMB_FACEBOOK_ACCESS_TOKEN_URL = os.environ['AMB_FACEBOOK_ACCESS_TOKEN_URL']
	AMB_FACEBOOK_AUTHORIZE_URL = os.environ['AMB_FACEBOOK_AUTHORIZE_URL']

	AMB_GOOGLE_APP_KEY = os.environ['AMB_GOOGLE_APP_KEY']
	AMB_GOOGLE_APP_SECRET = os.environ['AMB_GOOGLE_APP_SECRET']
	AMB_GOOGLE_ACCESS_TOKEN_URL = os.environ['AMB_GOOGLE_ACCESS_TOKEN_URL']
	AMB_GOOGLE_AUTHORIZE_URL = os.environ['AMB_GOOGLE_AUTHORIZE_URL']


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
