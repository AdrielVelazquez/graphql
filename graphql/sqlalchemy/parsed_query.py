from graphql.grammar_parser import parser
from graphql.sqlalchemy.class_registry import model_registry

def alchemy_data(graphql):
	'''
	Parses the data and does the query against the alchemy models
	'''
	#{'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': '1'}}
	graph_model = parser(graphql)
	alchemy_models = []
	model_name = graph_model.keys()[0]

	return None


def generate_select_statements(graph_model, model_name):
	select = []
	alchemy_model = model_registry.get(model_name)
	if not alchemy_model:
		raise ValueError("Defined model ({}) doesn't exist".format(model_name))
	for field_dict in graph_model.get(model_name, {}).get("fields"):
		if field_dict.get("child_fields"):
			temp_select = [getattr(alchemy_model, field_dict.get("field_name")]
		select.append()
