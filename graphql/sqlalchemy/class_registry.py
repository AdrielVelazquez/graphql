from dateutil import parser

model_registry = {}

def base_model_registry(base_model):
	"""Return class reference mapped to table.

	:param tablename: String with name of table.
	:return: Class reference or None.
	"""
	global model_registry
	for c in base_model._decl_class_registry.values():
		if hasattr(c, '__tablename__'):
			model_registry[c.__name__] = c


def session_registry(session):
	# Sessions aren't necessarily thread safe
	# It's advised that you take the proper precautions
	# in your application before registering sessions
	global model_registry
	model_registry["graphql_session"] = session


def column_type_graph(model, item, value):
	col_type = str(getattr(model, item).property.columns[0].type)
	if col_type == "INTEGER":
		return int(value)
	elif col_type.startswith("VARCHAR"):
		return str(value)


