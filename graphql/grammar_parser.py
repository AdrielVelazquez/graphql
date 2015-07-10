from parsimonious.grammar import Grammar

grammar = Grammar("""
     root =         WS object_name WS OPEN_ROUND WS object_parameter COLON object_id WS CLOSE_ROUND WS WS object WS
     object = OPEN_CURLY WS field_list WS CLOSE_CURLY
     WS =           ~"\s*"
     OPEN_CURLY =   "{"
     CLOSE_CURLY =  "}"
     OPEN_ROUND =   "("
     CLOSE_ROUND =   ")"
     COMMA = ","
     COLON = ":"
     object_name =  ~"[A-Z0-9_-]*"i
     object_id =    ~"[A-Z0-9_-]*"i
     object_parameter = ~"[A-Z0-9_-]*"i
     name =         ~"[A-Z0-9_-]*"i
     field_name =   ~"[A-Z0-9_-]*"i
     field_list = field WS (COMMA WS field)*
     field = field_name WS optional_object
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
    (object_name, object_parameter, object_id, my_object) = filter(filter_tokens, ast.children)

    return {
        object_name.text: {
            'fields': convert_object(my_object),
            object_parameter.text: object_id.text
        }
    }

def parser(graphql):
	# """User (id:234234) {one {sub1,sub2},two,three,four}"""
	# RETURN:
	# {'User': {'fields': [{'child_fields': [{'child_fields': [],
	#      'field_name': 'sub1'},
	#     {'child_fields': [], 'field_name': 'sub2'}],
	#    'field_name': 'one'},
	#   {'child_fields': [], 'field_name': 'two'},
	#   {'child_fields': [], 'field_name': 'three'},
	#   {'child_fields': [], 'field_name': 'four'}],
	#  'id': '234234'}}
    ast = grammar.parse(graphql)
    transformed_object =  convert_root_object(ast)
    return transformed_object
