from json import dumps # pragma: no cover
from sqlalchemy.orm import class_mapper # pragma: no cover
from app.models import User, Group # pragma: no cover

def serialize(obj, columns):
	# then we return their values in a dict
	return dict((c, getattr(obj, c)) for c in columns)

def queryAllToJson(model,conditions):
	# we can then use this for your particular example
	columns = [c.key for c in class_mapper(model).columns]
	serialized_objs = [
		serialize(obj,columns)
		for obj in model.query.filter_by(**conditions)
	]
	return dumps(serialized_objs)

def objectToJson(obj):
	columns = [c.key for c in class_mapper(obj.__class__).columns]
	serialized_obj = serialize(obj, columns)
	return dumps(serialized_obj)

def getUserId(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		raise Exception('username %s not found in database' % username)
	else:
		return user.id

def getGroupId(groupname):
	group = Group.query.filter_by(groupname=groupname).first()
	if group is None:
		raise Exception('groupname %s not found in database' % groupname)
	else:
		return group.id