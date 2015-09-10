from app import db
from app.models.base import Base

class Group(Base):
	__tablename__ = 'group_tbl'

	id = db.Column(db.Integer, db.ForeignKey('base_tbl.id'), primary_key=True)
	__mapper_args__ = {'polymorphic_identity': 'group'}
	groupname = db.Column(db.String(), unique=True, nullable=False)
	name = db.Column(db.String())

	def __init__(self, groupname, name):
		self.groupname = groupname
		self.name = name

	def __repr__(self):
		return '<groupname: {}, name: {}>'.format(self.groupname, self.name)
