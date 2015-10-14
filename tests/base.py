from flask.ext.testing import TestCase

from app import app, db
from app.models import Group, User, Command

class BaseTestCase(TestCase):
	"""A base test case."""

	def create_app(self):
		app.config.from_object('config.TestingConfig')
		return app

	def setUp(self):
		db.create_all()
		db.session.add(Group("global", "Global Group"))
		db.session.add(User("ghooo", "Mohamed", "Ghoneim", "ghooo", \
				"ghooo@cantkeepup.com"))
		db.session.add(User("omarayad1", "Omar", "Ayad", "omarayad1", \
				"omarayad1@cantkeepup.com"))
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
