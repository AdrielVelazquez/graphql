import copy

from sqlalchemy.orm.properties import RelationshipProperty

from graphql.grammar_parser import parser
from graphql.sqlalchemy.class_registry import model_registry, column_type_graph

def alchemy_data(graphql):
	'''
	Parses the data and does the query against the alchemy models
	'''
	#{'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': '1'}}
	graph_model = parser(graphql)
	select, where, joins = generate_model_and_restraints(graph_model)
	gsession = model_registry.get("graphql_session")
	results = gsession.query(*select)
	if joins:
		for join in joins:
			results = results.join(join)
	if where:
		results.filter(*where)
	return results.all()


def generate_model_and_restraints(graph_model):
	main_model = graph_model.keys()[0]
	alchemy_model = model_registry.get(main_model)
	restraint = copy.deepcopy(graph_model)
	restraint = restraint.get(main_model)
	restraint.pop("fields", None)
	where = []
	for key in restraint:
		value = column_type_graph(alchemy_model, key, restraint.get(key))
		where.append(getattr(alchemy_model, key) == value)
	if not alchemy_model:
		raise ValueError("Defined model ({}) doesn't exist".format(main_model))
	fields = graph_model.get(main_model).get("fields")
	select, joins = generate_select_joins(fields, alchemy_model)
	return select, where, joins



def generate_select_joins(fields, alchemy_model):
	#fields is a list of dictionaries
	select = []
	joins = []
	relationship_model = None
	for field in fields:
		getter_model = getattr(alchemy_model, field.get("field_name"))
		is_relationship = getattr(alchemy_model, field.get("field_name")).property
		if isinstance(is_relationship, RelationshipProperty):
			relationship_model = is_relationship.mapper.class_.__name__
			getter_model = model_registry.get(relationship_model)
			joins.append(getter_model)
		if field.get("child_fields"):
			temp_selects, temp_joins = generate_select_joins(field.get("child_fields"), getter_model)
			select.extend(temp_selects)
			joins.extend(temp_joins)
		else:
			select.append(getter_model)
	return select, joins




