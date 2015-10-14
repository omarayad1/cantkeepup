from app import db

class Base(db.Model):
	__tablename__ = 'base_tbl'
	
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(), nullable=False)
	__mapper_args__ = {'polymorphic_on': type}

	def __init__(self):
		pass

	def __repr__(self):
		return '<>'
