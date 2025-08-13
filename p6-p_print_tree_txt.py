import psycopg2
from datetime import datetime
import time, json, os
from dotenv import load_dotenv

global n_dotp, n_dotr
load_dotenv()

output_file = f"D:/VHP-Projects/vhp-serverless/output/vhptools/p_tree_structure.txt"
# output_file = f"/usr1/vhp_gittools/output/txt/p_tree_structure.txt"
# output_file = f"./test_tree.txt"

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
    # Fetch top-level or child modules based on parent_nr
    modules = fetch_child_modules(cursor, parent_nr)

    # Iterate through the modules and print the hierarchy
    for module in modules:
        id, modul_name, p_nr = module
        print(f"{'   ' * level}|-{modul_name} (ID: {id})")

        # Recursively fetch and print the child modules
        print_modules(cursor, p_nr, level + 1)

def print_modules_to_file(cursor, file, parent_nr=0, level=0):
    # Fetch top-level or child modules based on parent_nr
    modules = fetch_child_modules(cursor, parent_nr)

    # Iterate through the modules and write to the file
    for module in modules:
        
        id, modul_name, p_nr = module
        file.write(f"{'   ' * level}|-{modul_name} (ID: {p_nr})\n")

        # Recursively fetch and print the child modules to file
        print_modules_to_file(cursor, file, p_nr, level + 1)

# Main function to connect to the database and print all modules
def main():
    # Database connection details
    conn = psycopg2.connect(
        host =os.getenv("host"),
        database = os.getenv("database"),
        user = os.getenv("user"),
        password = os.getenv("password"),
    )
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    # generate txt tree
    # -------------------------------------------------------------------------------------------
    try:
        with open(output_file, "w", encoding='utf-8') as file:
            file.write(f"Modules Tree Structure ({timestamp}):\n")
            # print_modules_to_file(cursor, file, parent_nr=0)

        print(f"Tree structure has been successfully written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        pass
        # Close the database connection

    cursor.close()
    conn.close()

    try:
        with open(output_file, 'r') as file:
            # Read the content of the file
            content = file.read()
            # Print the content
            print(content)
    except FileNotFoundError:
        print(f"The file {file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


