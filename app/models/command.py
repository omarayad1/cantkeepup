from app import db

class Command(db.Model):
	__tablename__ = 'command_tbl'

	id = db.Column(db.Integer, primary_key=True)
	cmd_id = db.Column(db.String(), nullable=False)
	url = db.Column(db.String(), nullable=False)
	name = db.Column(db.String(), nullable=False)
	owner = db.Column(db.Integer, db.ForeignKey('base_tbl.id'), nullable=False)
	creator = db.Column(db.Integer, db.ForeignKey('user_tbl.id'), \
			nullable=False)

	__table_args__ = (db.UniqueConstraint('cmd_id', 'owner'),)

	def __init__(self, cmd_id, url, name, owner, creator):
 		self.cmd_id = cmd_id
 		self.url = url
 		self.name = name
 		self.owner = owner
 		self.creator = creator
 		
	def __repr__(self):
		return '<Name {}>'.format(self.name)
