from parsimonious.grammar import Grammar

grammar = Grammar("""
     root = operation WS OPEN_CURLY optional_alias WS object_name WS optional_attribute WS WS optional_object WS CLOSE_CURLY WS optional_fragment WS optional_object
     object =  OPEN_CURLY WS field_list WS CLOSE_CURLY
     WS = ~"\s*"
     OPEN_CURLY = "{"
     CLOSE_CURLY = "}"
     OPEN_ROUND = "("
     CLOSE_ROUND = ")"
     COMMA = ","
     COLON = ":"
     wild_card = ~"[A-Z0-9_-]*"i
     alias = object_name COLON
     attribute = object_parameter COLON object_id COMMA?
     multi_attribute = attribute+
     enclosed_attribute = OPEN_ROUND WS multi_attribute WS CLOSE_ROUND
     operation = ~"[A-Z0-9_-]*"i
     fragment = "fragment" WS wild_card WS "on" WS wild_card
     object_name = wild_card
     object_id = wild_card
     object_parameter = wild_card
     name = wild_card
     fragment_target = "..." wild_card
     field_name = wild_card
     field_list = field WS (COMMA WS field)*
     field = optional_alias WS (fragment_target / field_name) WS optional_attribute WS optional_object
     optional_alias = alias?
     optional_object = object?
     optional_attribute = enclosed_attribute?
     optional_fragment = fragment?
""")


IGNORE_NAMES = ['WS', 'OPEN_CURLY', 'CLOSE_CURLY', 'COMMA', 'COLON', 'OPEN_ROUND', 'CLOSE_ROUND']

split_list = lambda lst: (lst[0], lst[1:])

fragement_dict = {}

def filter_tokens(node):
    return node.expr_name not in IGNORE_NAMES


def convert_field(ast):
    (alias, _, field_name, _, attributes, _, optional_object) = ast
    child_fields = [] if len(optional_object.children) == 0 else (
        convert_object(optional_object.children[0])
    )
    convert_field_dict = {}
    if alias.text:
        convert_field_dict["alias"] = alias.text.strip(":")
    for attribute in attributes.children:
        temp_attribute = attribute.text.strip(",").strip("()")
        object_parameter, object_id = temp_attribute.split(":")
        if object_id.isdigit():
            object_id = int(object_id)
        convert_field_dict[object_parameter] = object_id
    if field_name.text.startswith("..."):
        fragement_term = field_name.text.replace("...", "")
        convert_field_dict["field_name"] = fragement_dict.get(fragement_term, [])
    else:
        convert_field_dict["field_name"] = field_name.text
    convert_field_dict["child_fields"] = child_fields
    return convert_field_dict

def convert_object(ast):
    ###Getting Correct filters###
    head, rest = [], []
    if filter(filter_tokens, ast.children):
        proper_len = 0
        filtered_children = None
        while proper_len != 2:
            if not filtered_children:
                filtered_children = filter(filter_tokens, filter(filter_tokens, ast.children)[0])
            else:
                filtered_children = filter(filter_tokens, filtered_children[0])
            proper_len = len(filtered_children)
        head, rest = filtered_children
    if not head or not rest:
        return []
    fields = [head] + map(lambda x: filter(filter_tokens, x.children)[0],
                          rest.children)
    fields = [convert_field(field) for field in fields]
    return fields


def convert_root_object(ast):
    (operation, alias, object_name, attributes, my_object, fragment, fragment_object) = filter(filter_tokens, ast.children)
    converted_dict = {operation.text: {}}
    if alias.text:
        converted_dict[operation.text]["alias"] = alias.text.strip(":")
    if fragment.text:
        _, fragment_name, _, model = fragment.text.split(" ")
        fragement_dict[fragment_name] = {"model": model, "fields": convert_object(fragment_object)}
    fields = convert_object(my_object)
    converted_dict[operation.text][object_name.text] = {'fields': fields}
    if attributes.children:
        attributes = filter(filter_tokens, attributes.children[0])[0]
    for attribute in attributes.children:
        temp_attribute = attribute.text.strip(",")
        object_parameter, object_id = temp_attribute.split(":")
        if object_id.isdigit():
            object_id = int(object_id)
        converted_dict[operation.text][object_name.text][object_parameter] = object_id
    return converted_dict

def parser(graphql):
    ast = grammar.parse(graphql)
    transformed_object =  convert_root_object(ast)
    return transformed_object
