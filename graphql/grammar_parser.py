from parsimonious.grammar import Grammar

grammar = Grammar("""
     root =         OPEN_CURLY optional_alias WS object_name WS OPEN_ROUND WS multi_attribute WS CLOSE_ROUND WS WS object WS CLOSE_CURLY
     object = OPEN_CURLY WS field_list WS CLOSE_CURLY
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
     object_name =  ~"[A-Z0-9_-]*"i
     object_id =    ~"[A-Z0-9_-]*"i
     object_parameter = ~"[A-Z0-9_-]*"i
     name =         ~"[A-Z0-9_-]*"i
     field_name =   ~"[A-Z0-9_-]*"i
     field_list = field WS (COMMA WS field)*
     field = field_name WS optional_object
     optional_alias = alias?
     optional_object = object?
""")


IGNORE_NAMES = ['WS', 'OPEN_CURLY', 'CLOSE_CURLY', 'COMMA', 'COLON', 'OPEN_ROUND', 'CLOSE_ROUND']

split_list = lambda lst: (lst[0], lst[1:])


def filter_tokens(node):
    return node.expr_name not in IGNORE_NAMES


def convert_field(ast):
    (field_name, _, optional_object) = ast

    child_fields = [] if len(optional_object.children) == 0 else (
        convert_object(optional_object.children[0])
    )

    return {
        'field_name': field_name.text,
        'child_fields': child_fields
    }


def convert_object(ast):
    head, rest = filter(filter_tokens, filter(filter_tokens, ast.children)[0])
    map(lambda x: filter(filter_tokens, x.children)[0], rest.children)

    fields = [head] + map(lambda x: filter(filter_tokens, x.children)[0],
                          rest.children)

    fields = [convert_field(field) for field in fields]
    return fields


def convert_root_object(ast):
    (alias, object_name, attributes, my_object) = filter(filter_tokens, ast.children)
    converted_dict = {}
    if alias.text:
        converted_dict["alias"] = alias.text
    converted_dict[object_name.text] = {'fields': convert_object(my_object),
        #object_parameter.text: object_id.text
    }
    for attribute in attributes.children:
        temp_attribute = attribute.text.strip(",")
        object_parameter, object_id = temp_attribute.split(":")
        converted_dict[object_name.text][object_parameter] = object_id
    return converted_dict

def parser(graphql):
    ast = grammar.parse(graphql)
    transformed_object =  convert_root_object(ast)
    return transformed_object
