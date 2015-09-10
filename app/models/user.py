from app import db
from app.models.base import Base

class User(Base):
	__tablename__ = 'user_tbl'

	id = db.Column(db.Integer, db.ForeignKey('base_tbl.id'), primary_key=True)
	__mapper_args__ = {'polymorphic_identity': 'user'}
	username = db.Column(db.String(), unique=True, nullable=False)
	firstname = db.Column(db.String())
	lastname = db.Column(db.String())

	def __init__(self, username, firstname, lastname):
		self.username = username
		self.firstname = firstname
		self.lastname = lastname

	def __repr__(self):
		return '<username: {}, name: {} {}>'.format(self.username, \
				self.firstname, self.lastname)
