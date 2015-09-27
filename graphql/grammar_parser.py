import copy
from parsimonious.grammar import Grammar

grammar = Grammar("""
     root = operation WS OPEN_CURLY optional_alias WS object_name WS optional_attribute WS WS optional_object WS CLOSE_CURLY WS multi_fragment 
     object =  OPEN_CURLY WS field_list WS CLOSE_CURLY
     WS = ~"\s*"
     OPEN_CURLY = "{"
     CLOSE_CURLY = "}"
     OPEN_ROUND = "("
     CLOSE_ROUND = ")"
     COMMA = ","
     COLON = ":"
     OPEN_SQUARE = "["
     CLOSE_SQUARE = "]"
     wild_card = ~"[A-Z0-9_-]*"i
     listed_wildcard = wild_card COMMA?
     wild_card_list = OPEN_SQUARE WS listed_wildcard+ WS CLOSE_SQUARE
     alias = object_name COLON
     attribute = object_parameter COLON object_id COMMA?
     multi_attribute = attribute+
     fragment_plus_object = optional_fragment WS optional_object
     multi_fragment = fragment_plus_object+
     enclosed_attribute = OPEN_ROUND WS multi_attribute WS CLOSE_ROUND
     operation = ~"[A-Z0-9_-]*"i
     fragment = "fragment" WS wild_card WS "on" WS wild_card
     object_name = wild_card
     object_id = wild_card_list / wild_card 
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


IGNORE_NAMES = ['WS', 'OPEN_CURLY', 'CLOSE_CURLY', 'COMMA', 'COLON', 'OPEN_ROUND', 'CLOSE_ROUND', 'OPEN_SQUARE', 'CLOSE_SQUARE']

split_list = lambda lst: (lst[0], lst[1:])

fragement_dict = {}

def filter_tokens(node):
    return node.expr_name not in IGNORE_NAMES

def convert_item(s):
    if s.isdigit():
        return int(s)
    try:
        returned_item = float(s)
        return returned_item
    except ValueError:
        if s.startswith("["):
            s.strip("[]")
        return str(s)

def convert_field(ast, target_object):
    final_list = []
    (alias, _, field_name, _, attributes, _, optional_object) = ast
    child_fields = [] if len(optional_object.children) == 0 else (
        convert_object(optional_object.children[0], target_object)
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
        assert fragement_term in fragement_dict, "fragement {} isn't in fragement dict ({})".format(fragement_term, ", ".join(fragement_dict.keys()))
        assert target_object == fragement_dict.get(fragement_term).get("model"), "fragement target {} isn't in fragement dict ({})".format(target_object, fragement_dict.get(fragement_term).get("model"))
        for frag_field in fragement_dict.get(fragement_term).get("fields"):
            temp_dict = copy.deepcopy(convert_field_dict)
            temp_dict["field_name"] = frag_field.get("field_name")
            temp_dict["child_fields"] = frag_field.get("child_fields")
            final_list.append(temp_dict)
    else:
        convert_field_dict["field_name"] = field_name.text
        convert_field_dict["child_fields"] = child_fields
        final_list.append(convert_field_dict)
    return final_list

def convert_object(ast, target_object):
    ###Getting Correct filters###
    head, rest = [], []
    if filter(filter_tokens, ast.children):
        proper_len = 0
        filtered_children = None
        while proper_len != 2:
            '''
            nested children sometimes get nested deeper then the immediate level
            After parsing and filtering, two objects should remain. 
            '''
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
    returned_fields = []
    for field in fields:
        for nested_field in convert_field(field, target_object):
            returned_fields.append(nested_field)
    return returned_fields


def convert_root_object(ast):
    (operation, alias, object_name, attributes, my_object, fragment) = filter(filter_tokens, ast.children)
    converted_dict = {operation.text: {}}
    if alias.text:
        converted_dict[operation.text]["alias"] = alias.text.strip(":")
    for frag in filter(filter_tokens, filter(filter_tokens, fragment.children)):
        if "".join(frag.text.split()):
            frag_text, frag_object = filter(filter_tokens, frag.children)
            _, fragment_name, _, model = frag_text.text.split(" ")
            fragement_dict[fragment_name] = {"model": model, "fields": convert_object(frag_object, model)}
    fields = convert_object(my_object, object_name.text)
    converted_dict[operation.text][object_name.text] = {'fields': fields}
    if attributes.children:
        attributes = filter(filter_tokens, attributes.children[0])[0]
    for attribute in attributes.children:
        filtered_attribute = filter(filter_tokens, attribute)
        object_parameter = filtered_attribute[0]
        object_id = filtered_attribute[1]
        #Check if object id is a list
        if object_id.children[0].expr_name == "wild_card_list":
            object_id = object_id.text.strip("[()]").split(",")
            object_id = map(convert_object, object_id)
        elif object_id.text.isdigit():
            object_id = int(object_id.text)
        else:
            object_id = object_id.text
        converted_dict[operation.text][object_name.text][object_parameter.text] = object_id
    return converted_dict

def parser(graphql):
    ast = grammar.parse(graphql)
    transformed_object = convert_root_object(ast)
    return transformed_object
