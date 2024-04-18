import sqlite3


def dfs(id_parent_node):
    childs = get_childs(id_parent_node)
    if childs:
        for child in childs:
            print(child)
            dfs(child[0])


def DFGH():
    conn = sqlite3.connect("example.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Project_structure_of_nodes;
    """)
    
    return [dict(row) for row in cursor.fetchall()]


def get_childs(id_parent_node):
    conn = sqlite3.connect("example.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """
    SELECT id_node FROM Project_structure_of_nodes
    WHERE id_parent = ?
    """
    cursor.execute(sql, [id_parent_node])
    result = cursor.fetchall()
    conn.close()
    return result


def main():
    #dfs(get_project_node())
    print(DFGH())


main()


#
'''
conn.row_factory = sqlite3.Row
result = [dict(row) for row in cursor.fetchall()]
'''