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