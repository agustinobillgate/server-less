# service,function
# getSupplierList,prepare_supply_listbl
# getPreparePurchaseOrderList,prepare_po_listbl
# getPurchaseOrderList,get_po_listbl
# addSupplier,mk_supply_btn_gobl_1

import os
import psycopg2
import datetime 
import time, json, os
from dotenv import load_dotenv


load_dotenv()
folder_modules = f"D:/VHP-Projects/vhp-serverless/modules"


conn = psycopg2.connect(
    "host": os.getenv("host"),
    "database": os.getenv("database"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
)
cursor = conn.cursor()

def close_connection():
    cursor.close()
    conn.close()

def list_directories(path):
    # List all entries in the directory
    entries = os.listdir(path)
    
    # Filter out directories only
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    
    return directories

def find_file(base_folder, file_name):
    # Convert the file_name to lowercase
    file_name = file_name.lower()
    for root, dirs, files in os.walk(base_folder.lower()):
        root_lower = root.lower()
        for file in files:
            if file.lower() == file_name:  # Check case-insensitively
                file_path = os.path.join(root_lower, file.lower())  # Get the full lowercase path
                return file_path  
    return ""


def get_file_info(file_path):
    try:
        file_size = os.path.getsize(file_path)
        file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            num_lines = sum(1 for _ in file)
        return file_size, file_date, num_lines
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None


def convert_backslashes(file_path):
    if file_path is not None:
        return file_path.replace('\\', '/')
    else:
        return file_path

def update_p_path():
    cursor.execute("SELECT p_filename, id FROM mapping ;")
    filenames = cursor.fetchall()

    for filename_tuple in filenames:
        p_filename = filename_tuple[0].lower()
        
        # Search for the file
        file_path = find_file(folder_p, p_filename)
        file_path2 = convert_backslashes(file_path)
        
        if file_path2:
            # Update the database with the found file path
            file_size, file_date, number_of_lines = get_file_info(file_path2)
            # print(p_filename, file_date, number_of_lines)
            update_p_path_in_db(cursor, conn, p_filename, file_path2, file_size, file_date, number_of_lines)
        else:
            update_p_path_in_db(cursor, conn, p_filename, "not found.", 0, '1970-01-01 00:00:00', 0)
            # update_p_path_in_db(cursor, conn, p_filename, file_path, file_size, file_date, number_of_lines)
            print(f"File {file_path}/{p_filename} not found.")
            


def update_p_path_in_db(cursor, conn, p_path, p_filename, file_size, file_date, number_of_lines):
    """Update the p_path field in the mapping table."""
    update_query = """
    UPDATE mapping
    SET p_path = %s, p_size=%s, p_date=%s, p_lines=%s
    WHERE p_filename = %s;
    """
     # Print the final query with the parameters substituted for debugging
    p_filename = os.path.basename(p_filename).lower()
    # final_query = update_query % (
    #     repr(p_path),  # Use repr to show the string with quotes
    #     repr(file_size),
    #     repr(file_date),
    #     repr(number_of_lines),
    #     repr(p_filename)
    # )
    
    # print("Executing SQL query:")
    # print(final_query)
    cursor.execute(update_query, (p_path, file_size, file_date, number_of_lines, p_filename ))
    conn.commit()


def load_mapping_file():
    # Get the list of directories
    directories = list_directories(folder_modules)
    # print(directories)
    # Print the directory names
    sql_update = """
                    truncate table mapping;
                    """
    cursor.execute(sql_update)
    conn.commit()

    for directory in directories:
        
        vhp_module = directory
        mapping_file = f"{folder_modules}/{vhp_module}/_mapping.txt"
        # print(directory, mapping_file)
        # Read the mapping file and process it
        with open(mapping_file, 'r') as file:
            # Skip the header
            next(file)
            
            # Prepare the insert query
            insert_query = """
            INSERT INTO mapping (vhp_module, endpoint, py_filename)
            VALUES (%s, %s, %s);
            """
            
            # Read and insert each line of data
            for line in file:
                endpoint, py_filename = line.strip().split(',')
                cursor.execute(insert_query, (vhp_module, endpoint, py_filename))

        # Commit the transaction to save changes
        conn.commit()


    # update the p_filename
    sql_update = """
                    update mapping set p_filename = CONCAT(REPLACE(py_filename, '_', '-'), '.p');
                    """
    cursor.execute(sql_update)
    conn.commit()
    print("Data imported successfully.")

# get .p fullpath and filesize 
folder_p = f"D:/VHP-Projects/vhp-master-source/Master"
# load_mapping_file()
update_p_path()

# Close the database connection
cursor.close()
conn.close()


close_connection()
