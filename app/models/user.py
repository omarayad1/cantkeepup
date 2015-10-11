from app import db, bcrypt
from app.models.base import Base

class User(Base):
	__tablename__ = 'user_tbl'

	id = db.Column(db.Integer, db.ForeignKey('base_tbl.id'), primary_key=True)
	__mapper_args__ = {'polymorphic_identity': 'user'}
	username = db.Column(db.String(), unique=True, nullable=False)
	firstname = db.Column(db.String(), nullable=False)
	lastname = db.Column(db.String(), nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)

	def __init__(self, username, firstname, lastname, password, email):
		self.username = username
		self.firstname = firstname
		self.lastname = lastname
		self.password = bcrypt.generate_password_hash(password)
		self.email = email

	def __repr__(self):
		return '<username: {}, name: {} {}>'.format(self.username, \
				self.firstname, self.lastname)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)