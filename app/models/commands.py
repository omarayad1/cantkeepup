from app import db

class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cmd_id = db.Column(db.String())
    url = db.Column(db.String())
    name = db.Column(db.String())

    def __repr__(self):
   		return '<Name %r>' % (self.name)
