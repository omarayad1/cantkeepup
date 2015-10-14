from json import dumps
from sqlalchemy.orm import class_mapper

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
