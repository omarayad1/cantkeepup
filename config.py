import os


class Config(object):
	basedir = os.path.abspath(os.path.dirname(__file__))

	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

class ProductionConfig(Config):
	DEBUG = False


class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

# to us this you have to add this environment variable
# export APP_SETTINGS="config.DevelopmentConfig"
# one way to add it to postactivate of your virtualenv
class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True


class TestingConfig(Config):
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'