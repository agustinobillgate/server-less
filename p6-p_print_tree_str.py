import psycopg2
from datetime import datetime

# output_file = f"/usr1/vhptools/git_source/output/txt/p_tree_structure.txt"
# output_file = f"D:/docker/tmpgit/output/txt/p_tree_structure.txt"
output_file = f"D:/VHP-Projects/vhp-serverless/output/vhptools/p_tree_structure.txt"
# output_file = f"./test_tree.txt"

tree_content = ""
def fetch_child_modules(cursor, parent_nr):
    query = """
    SELECT id, modul_name, p_nr
    FROM p_trees
    WHERE parent_nr = %s
    ORDER BY id;
    """
    cursor.execute(query, (parent_nr,))
    return cursor.fetchall()

# Function to print modules iteratively
def print_modules(cursor, parent_nr=0, level=0):
    global tree_content
    # Fetch top-level or child modules based on parent_nr
    modules = fetch_child_modules(cursor, parent_nr)

    # Iterate through the modules and print the hierarchy
    for module in modules:
        id, modul_name, p_nr = module
        print(f"{'   ' * level}|-{modul_name} (ID: {id})")

        # Recursively fetch and print the child modules
        print_modules(cursor, p_nr, level + 1)

def print_modules_to_file(cursor, parent_nr=0, level=0):
    global tree_content
    # Fetch top-level or child modules based on parent_nr
    modules = fetch_child_modules(cursor, parent_nr)

    # Iterate through the modules and write to the file
    for module in modules:
        
        id, modul_name, p_nr = module
        tree_content += f"{'   ' * level}|-{modul_name} (ID: {p_nr})\n"

        # Recursively fetch and print the child modules to file
        print_modules_to_file(cursor, p_nr, level + 1)

# Main function to connect to the database and print all modules
def main():
    global tree_content
    # Database connection details
    conn = psycopg2.connect(
        # host = "vhp-devtest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com",
        # database = "vhptools",
        # user = "vhpadmin",
        # password = "bFdq8QsQoxH1vAvO"
        # host = "localhost",
        # database = "vhptools",
        # user = "postgres",
        # password = "bali2000"
        host = "psql.staging.e1-vhp.com",
        database = "vhptools",
        user = "postgres",
        password = "DevPostgreSQL#2024",

    )
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    # generate txt tree
    # -------------------------------------------------------------------------------------------
    tree_content = f"Modules Tree Structure ({timestamp}):\n"
    print_modules_to_file(cursor, parent_nr=51790)

    print(tree_content)
    cursor.close()
    conn.close()

    

if __name__ == "__main__":
    main()


