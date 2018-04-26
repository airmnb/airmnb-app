
import logging
import os

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_AMB_DATABASE_URI = os.environ['AMB_DATABASE_URI']
	LOG_LEVEL = logging.INFO
	SECRET_KEY = 'something unique and secret'

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	LOG_LEVEL = logging.DEBUG
	AMB_GOOGLE_APP_KEY = os.environ['AMB_GOOGLE_APP_KEY']
	AMB_GOOGLE_APP_SECRET = os.environ['AMB_GOOGLE_APP_SECRET']
	AMB_GOOGLE_TOKEN_ENDPOINT = os.environ['AMB_GOOGLE_TOKEN_ENDPOINT']
	AMB_GOOGLE_AUTHORIZATION_URL = os.environ['AMB_GOOGLE_AUTHORIZATION_URL']


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
