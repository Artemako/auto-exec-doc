import sqlite3

def dfs(id_parent_node):
    childs = get_childs(id_parent_node)
    if childs:
        for child in childs:
            print(child)
            dfs(child[0])


def get_project_node():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id_node FROM Project_structure_of_nodes
    WHERE type_node = "PROJECT";
    """)
    return cursor.fetchone()[0]

def get_childs(id_parent_node):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    sql = """
    SELECT id_node FROM Project_structure_of_nodes
    WHERE id_parent = ?
    """
    cursor.execute(sql, [id_parent_node])
    return cursor.fetchall()

def main():
    dfs(get_project_node())



main()