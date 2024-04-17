nodes = [
    
    (0, "Проект", None, "PROJECT", None, None, ""),
    (1204, "ПТ-4", 12, "FORM", 1203, 1205, "main"),
    (1205, "ПТ-5", 12, "FORM", 1204, 1206, "main"),
    (1206, "ПТ-6", 12, "FORM", 1205, 1207, "main"),
    (1207, "ПТ-7", 12, "FORM", 1206, 1208, "main"),
    (1208, "ПТ-8", 12, "FORM", 1207, 1209, "main"),
    (12, "Паспорт трассы", 0, "GROUP", 11, None, None),
    (1201, "ПТ-1", 12, "FORM", None, 1202, "main"),
    (1202, "ПТ-2", 12, "FORM", 1201, 1203, "main"),
    (1203, "ПТ-3", 12, "FORM", 1202, 1204, "main"),
    (1205, "ПТ-5", 12, "FORM", 1204, 1206, "main"),
    (1206, "ПТ-6", 12, "FORM", 1205, 1207, "main"),
    (1207, "ПТ-7", 12, "FORM", 1206, 1208, "main"),
    (1209, "ПТ-9", 12, "FORM", 1208, 1210, "main"),
    (1210, "ПТ-10", 12, "FORM", 1209, 1211, "main"),
    (10, "Титульный лист", 0, "FORM", None, 11, "main"),
    (11, "Реестр документации", 0, "FORM", 10, 12, "main"),    
    (1204, "ПТ-4", 12, "FORM", 1203, 1205, "main"),
    (1208, "ПТ-8", 12, "FORM", 1207, 1209, "main"),
    (1209, "ПТ-9", 12, "FORM", 1208, 1210, "main"),
    (1210, "ПТ-10", 12, "FORM", 1209, 1211, "main"),
]
# "id_node": elem[0],
# "name_node": elem[1],
# "id_parent": elem[2],
# "type_node": elem[3],
# "id_left": elem[4],
# "id_right": elem[5],
# "template_name": elem[6],

def traversal(parent_node):
    print(parent_node)
    childs = list(filter(lambda node: node[2] == parent_node[0], nodes))
    #print(parent_node, childs)
    if childs:
        node = get_left_child(childs)
        while id_right_node(node):
            traversal(node)
            node = nodes[]
    return None


def get_left_child(childs):
    left_child = None
    for child in childs:
        if not child[4]:
            left_child = child
            return left_child

def id_right_node(node):
    return node[5]




traversal(nodes[0])