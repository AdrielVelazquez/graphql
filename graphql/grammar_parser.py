from parsimonious.grammar import Grammar

grammar = Grammar("""
     root =         operation WS OPEN_CURLY optional_alias WS object_name WS optional_attribute WS WS optional_object WS CLOSE_CURLY
     object =  OPEN_CURLY WS field_list WS CLOSE_CURLY
     WS =           ~"\s*"
     OPEN_CURLY =   "{"
     CLOSE_CURLY =  "}"
     OPEN_ROUND =   "("
     CLOSE_ROUND =   ")"
     COMMA = ","
     COLON = ":"
     alias = object_name COLON
     attribute = object_parameter COLON object_id COMMA?
     multi_attribute = attribute+
     enclosed_attribute = OPEN_ROUND WS multi_attribute WS CLOSE_ROUND
     operation = ~"[A-Z0-9_-]*"i
     object_name =  ~"[A-Z0-9_-]*"i
     object_id =    ~"[A-Z0-9_-]*"i
     object_parameter = ~"[A-Z0-9_-]*"i
     name =         ~"[A-Z0-9_-]*"i
     field_name =   ~"[A-Z0-9_-]*"i
     field_list = field WS (COMMA WS field)*
     field = optional_alias WS field_name WS optional_attribute WS optional_object
     optional_alias = alias?
     optional_object = object?
     optional_attribute = enclosed_attribute?
""")


IGNORE_NAMES = ['WS', 'OPEN_CURLY', 'CLOSE_CURLY', 'COMMA', 'COLON', 'OPEN_ROUND', 'CLOSE_ROUND']

split_list = lambda lst: (lst[0], lst[1:])


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
    (operation, alias, object_name, attributes, my_object) = filter(filter_tokens, ast.children)
    converted_dict = {operation.text: {}}
    if alias.text:
        converted_dict[operation.text]["alias"] = alias.text.strip(":")
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
